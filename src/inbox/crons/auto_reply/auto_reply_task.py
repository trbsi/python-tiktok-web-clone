import random
import re
from threading import Lock

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer

from app import settings
from src.inbox.models import Message, Conversation
from src.inbox.services.inbox_settings.inbox_settings_service import InboxSettingsService


class AutoReplyTask:
    #  class attribute (shared by all instances)
    _model = None
    _tokenizer = None
    _lock = Lock()

    def __init__(
            self,
            inbox_settings_service: InboxSettingsService | None = None,
    ):
        if self._model is None:
            with self._lock:
                if self._model is None:
                    self._load_model()
        self.inbox_settings_service = inbox_settings_service or InboxSettingsService()

    def auto_reply(self, message_id: int, send_message_service):
        message: Message = Message.objects.get(id=message_id)

        # if creator sent a message do not auto reply
        if message.sender.is_creator():
            return

        conversation: Conversation = message.conversation
        creator = conversation.get_creator()

        auto_reply_active = self.inbox_settings_service.is_auto_reply_active(user=creator)
        if auto_reply_active == False:
            return

        # Get last 50 messages as context
        last_messages = (
            Message.objects
            .select_related('sender')
            .filter(conversation=conversation)
            .filter(id__lte=message_id)
            .order_by('-id')[:50]
        )
        last_messages = last_messages.reverse()

        # Create GPT format
        chat_history = []
        for message in last_messages:
            if message.sender.is_creator():
                role = 'assistant'
            else:
                role = 'user'

            chat_history.append({'role': role, 'content': message.message})

        # Get reply and save
        reply = self._get_reply_from_ai(chat_history)
        replies = self._split_sentences_randomly(reply)

        for reply in replies:
            send_message_service.send_message(
                user=creator,
                conversation_id=conversation.id,
                message_content=reply,
            )

    def _load_model(self) -> None:
        # -------------------- PRELOAD MODEL AND TOKENIZER --------------------
        base_model = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # or your TinyLlama
        adapter_path = f"{settings.BASE_DIR}/gpt/trained_model"  # path to your LoRA adapter

        # -------------------- Load tokenizer --------------------
        tokenizer = AutoTokenizer.from_pretrained(base_model)
        # Fix pad token if missing
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        # -------------------- Load model + LoRA --------------------
        model = AutoModelForCausalLM.from_pretrained(
            base_model,
            device_map="auto",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )

        model = PeftModel.from_pretrained(model, adapter_path)
        model.eval()  # evaluation mode

        # Assign to class attribute so it is reused by all instances
        AutoReplyTask._model = model
        AutoReplyTask._tokenizer = tokenizer

    def _get_reply_from_ai(self, chat_history) -> str:
        # -------------------- Build input text --------------------
        style_instruction = "Assistant should respond in short, casual sentences.\n\n"
        input_text = style_instruction + self._tokenizer.apply_chat_template(
            chat_history,
            tokenize=False,
            add_generation_prompt=True  # model continues as assistant
        )

        inputs = self._tokenizer(input_text, return_tensors="pt").to(self.model.device)

        # -------------------- Generate reply --------------------
        outputs = self._model.generate(
            **inputs,
            max_new_tokens=50,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=self._tokenizer.eos_token_id,
            eos_token_id=self._tokenizer.eos_token_id
        )

        # --- Only decode newly generated tokens ---
        generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]
        reply = self._tokenizer.decode(generated_tokens, skip_special_tokens=True)

        return reply

    def _split_sentences_randomly(self, text: str, max_sentences=5):
        text = text.casefold()  # lowercase

        # Split by sentence-ending punctuation (., ?, !)
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        sentences = [s.strip() for s in sentences if s.strip()]

        # Take at most the first 5 sentences
        sentences = sentences[:max_sentences]

        # Randomly merge some sentences (at most 2 each)
        merged = []
        i = 0
        while i < len(sentences):
            # Randomly decide to merge with the next one (50% chance)
            if i < len(sentences) - 1 and random.choice([True, False]):
                temp_msg = (f"{sentences[i]} {sentences[i + 1]}")
                i += 2
            else:
                temp_msg = (sentences[i])
                i += 1

            temp_msg = temp_msg.rstrip('.').rstrip('!')
            merged.append(temp_msg)

        return merged
