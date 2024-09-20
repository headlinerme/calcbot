from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq


router_start = Router()


@router_start.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await rq.set_user(message.from_user.id)
    await rq.set_user_data(message.from_user.id, "", 0, 0, 0, "", "", {"standard":{"calories": "-","proteins": "-","fats": "-","carbohydrates": "-"}})
    
    await message.bot.send_chat_action(
        chat_id=message.from_user.id, 
        action=ChatAction.TYPING
    )
    await message.answer(
        text=f"<strong>Привет, {message.from_user.first_name}!👋🏻\n\
Я Ваш персональный бот-диетолог.</strong>\n\n\
<strong>🗒️ Что я умею?</strong>\n\
• Рассчитаю калории и БЖУ для Ваших любимых блюд\n\
• Поделюсь советами по следующим приемам пищи\n\
• Помогу сбалансировать питание и сделать его максимально здоровым и разнообразным",
        parse_mode="HTML",
        reply_markup=kb.main
    )
    await state.clear()
