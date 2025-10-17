from celery import shared_task
from transformers import AutoTokenizer, AutoModelForCausalLM

from app import settings
from src.inbox.crons.auto_reply.auto_reply_task import AutoReplyTask

model_path = settings.BASE_DIR + 'gpt/dialo_model'
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)


@shared_task
def auto_reply(message_id: int):
    task = AutoReplyTask(tokenizer=tokenizer, model=model)
    task.auto_reply(message_id)
