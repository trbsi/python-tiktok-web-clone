from celery import shared_task
from transformers import AutoTokenizer, AutoModelForCausalLM

from app import settings
from src.inbox.crons.auto_reply.auto_reply_task import AutoReplyTask

model_path = f'{settings.BASE_DIR}/gpt/trained_model'
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)


@shared_task
def task_auto_reply(message_id: int, send_message_service):
    task = AutoReplyTask(tokenizer=tokenizer, model=model)
    task.auto_reply(message_id, send_message_service)
