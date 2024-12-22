
from aiogram import F, Router
from aiogram.types import ChatPermissions, CallbackQuery
from .welcome import welcome_messages, verification_tasks

router = Router()

@router.callback_query(F.data.startswith("agree_"))
async def process_agree(callback: CallbackQuery):
    _, chat_id, user_id = callback.data.split('_')
    if int(user_id) != callback.from_user.id:
        await callback.answer("This verification is not for you", show_alert=True)
        return

    chat_id_int = int(chat_id)
    user_id_int = int(user_id)

    if user_id_int in verification_tasks:
        verification_tasks[user_id_int].cancel()
        del verification_tasks[user_id_int]


    await callback.message.bot.restrict_chat_member(
        chat_id=chat_id_int,
        user_id=user_id_int,
        permissions=ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
    )

    if user_id_int in welcome_messages:
        await callback.message.bot.delete_message(
            chat_id=chat_id_int,
            message_id=welcome_messages[user_id_int]
        )
        del welcome_messages[user_id_int]

    await callback.message.edit_text("✅ You've been verified! You can now chat in the group")
    await callback.answer()