import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import ContentTypeFilter


router = Router()
logger = logging.getLogger(__name__)

@router.message(ContentTypeFilter(content_types={
    'new_chat_members', 'left_chat_member', 'new_chat_title', 
    'new_chat_photo', 'delete_chat_photo', 'pinned_message'
}))
async def handle_service_message(message: Message):
    await message.delete()
    logger.info(f"Deleted service message: {message.message_id}")