from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

RULES_TEXT = """
📜 *Group Rules*

1. Be respectful to all members
2. No spam or self-promotion
3. No NSFW content
4. No hate speech or harassment
5. Only use English in chat
6. Follow admins' instructions

Please read the rules carefully and click Agree to join the chat.
"""

def get_rules_keyboard(user_id: int, chat_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="✅ I Agree", 
            callback_data=f"agree_{chat_id}_{user_id}"
        )
    ]])
