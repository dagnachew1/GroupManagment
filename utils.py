
from aiogram import types

async def get_user_id(message: types.Message) -> int:
    if message.reply_to_message:
        return message.reply_to_message.from_user.id

    parts = message.text.split()
    if len(parts) < 2:
        raise ValueError
    return int(parts[1])

async def check_admin(message: types.Message) -> bool:
    if message.chat.type in ['group', 'supergroup']:
        admin = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        return admin.status in ['administrator', 'creator']
    return False