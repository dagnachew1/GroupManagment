from aiogram import Router
from aiogram.types import Message, ChatPermissions
from aiogram.filters import Command, CommandStart, CommandObject

from filters import IsAdmin, IsValidTarget
from .messages import RULES_TEXT, get_rules_keyboard

router = Router()

@router.message(CommandStart(deep_link=True))
async def start_command(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("Hi! I'm a group management bot")
        return
        
    if command.args.startswith('verify_'):
        _, chat_id, user_id = command.args.split('_')
        if int(user_id) != message.from_user.id:
            await message.answer("This verification link is not for you!")
            return

        await message.answer(
            RULES_TEXT, 
            reply_markup=get_rules_keyboard(user_id, chat_id)
        )

@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "Admin commands:\n"
        "/ban - Ban a user\n"
        "/unban - Unban a user\n"
        "/mute - Mute a user\n"
        "/unmute - Unmute a user"
    )

@router.message(Command("ban"), IsAdmin(), IsValidTarget())
async def ban_command(message: Message, user_id: int):
    reason = message.text.replace("/ban", "", 1).strip()

    await message.bot.ban_chat_member(
        chat_id=message.chat.id,
        user_id=user_id
    )
    
    response_text = f"User {user_id} has been banned."
    if reason:
        response_text += f"\n<b>Reason:</b> {reason}"
    
    await message.answer(response_text)

@router.message(Command("unban"), IsAdmin(), IsValidTarget())
async def unban_command(message: Message, user_id: int):
    await message.bot.unban_chat_member(
        chat_id=message.chat.id,
        user_id=user_id
    )
    await message.answer(f"User {user_id} is unbanned.")

@router.message(Command("mute"), IsAdmin(), IsValidTarget())
async def mute_command(message: Message, user_id: int):
    reason = message.text.replace("/mute", "", 1).strip()

    await message.bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=user_id,
        permissions=ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False
        )
    )
    
    response_text = f"User {user_id} has been muted."
    if reason:
        response_text += f"\n<b>Reason:</b> {reason}"
    
    await message.answer(response_text)

@router.message(Command("unmute"), IsAdmin(), IsValidTarget())
async def unmute_command(message: Message, user_id: int):
    await message.bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=user_id,
        permissions=ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
    )
    await message.answer(f"User {user_id} is unmuted")