from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatAction


router_support = Router()


# Техподдержка    
@router_support.message(F.text == "Техподдержка")
async def support(message: Message):
    await message.bot.send_chat_action(
        chat_id=message.from_user.id, 
        action=ChatAction.TYPING
    )
    await message.answer(
        text=f"{message.from_user.first_name}, возникла проблема?\n\nНапишите одному из разработчиков:\n@headlinerme_dev\n@texmansport"
    )
