from aiogram.filters import BaseFilter
from aiogram.types import Message

from utils import check_admin

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return await check_admin(message)

class IsValidTarget(BaseFilter):
    async def __call__(self, message: Message) -> dict:
        if not message.reply_to_message:
            await message.reply("Please reply to a message!")
            return False
            
        user_id = message.reply_to_message.from_user.id
        
        if user_id == message.bot.id:
            await message.reply("Sorry, I can't do that!")
            return False
            
        chat_member = await message.bot.get_chat_member(message.chat.id, user_id)
        if chat_member.status in ['administrator', 'creator']:
            await message.reply("Sorry, I can't do that!")
            return False
            
        return {"user_id": user_id}