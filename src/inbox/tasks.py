import torch
from celery import shared_task
from peft import PeftModel
from transformers import AutoModelForCausalLM
from transformers import AutoTokenizer

from app import settings
from src.inbox.crons.auto_reply.auto_reply_task import AutoReplyTask

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


@shared_task
def task_auto_reply(message_id: int, send_message_service):
    task = AutoReplyTask(tokenizer=tokenizer, model=model)
    task.auto_reply(message_id, send_message_service)
