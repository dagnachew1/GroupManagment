from aiogram import Router, Bot, F
import asyncio
from aiogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    ChatPermissions,
    Message
)
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram.types.chat_member_updated import ChatMemberUpdated
from aiogram.fsm.context import FSMContext
from states import VerificationStates
from typing import Dict

router = Router()
welcome_messages: Dict[int, int] = {}
verification_tasks: Dict[int, asyncio.Task] = {}  

async def handle_verification_timeout(bot: Bot, chat_id: int, user_id: int):
    await asyncio.sleep(666)
    try:

        await bot.ban_chat_member(chat_id, user_id)
        await bot.unban_chat_member(chat_id, user_id) 
        if user_id in welcome_messages:
            await bot.delete_message(chat_id, welcome_messages[user_id])
            del welcome_messages[user_id]

    finally:
        if user_id in verification_tasks:
            del verification_tasks[user_id]

@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_join(event: ChatMemberUpdated, bot: Bot, state: FSMContext):
    user = event.new_chat_member.user
    chat = event.chat
    
    if user.is_bot:
        return

    bot_info = await bot.get_me()
    start_link = f"https://t.me/{bot_info.username}?start=verify_{chat.id}_{user.id}"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="📜 Verify Yourself", url=start_link)
    ]])
    
    await bot.restrict_chat_member(
        chat.id, 
        user.id,
        permissions=ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False
        )
    )
    
    await state.set_state(VerificationStates.waiting_verification)
    await state.update_data(chat_id=chat.id)
    
    msg = await bot.send_message(
        chat.id,
        f"Welcome <a href='tg://user?id={user.id}'>{user.full_name}</a>! Please verify yourself by reading our rules",
        reply_markup=keyboard
    )
    welcome_messages[user.id] = msg.message_id

    verification_tasks[user.id] = asyncio.create_task(
        handle_verification_timeout(bot, chat.id, user.id)
    )

@router.message(F.new_chat_members)
async def welcome_new_member(message: Message):
    for new_member in message.new_chat_members:
        msg = await message.answer(
            f"Welcome {new_member.mention_html()}! Please verify yourself by clicking the button below"
        )
        welcome_messages[new_member.id] = msg.message_id
