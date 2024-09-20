from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext

from pytz import timezone

import app.keyboards as kb
from app.states import Request
import app.database.requests as rq
from app.calculations.calc_calories import calc_calories


router_calculation = Router()


@router_calculation.message(F.text == "Расчет КБЖУ")
async def calc(message: Message, state: FSMContext):
    await message.bot.send_chat_action(
        chat_id=message.from_user.id, 
        action=ChatAction.TYPING
    )
    await message.answer(
        text="Введите название блюда, список ингредиентов и вес, а я дам полную информацию о его пищевой ценности.\n\n\
<strong>Формат ввода данных:</strong>\n\
✅ - гречневая каша с молоком: вареная гречневая каша 300 грамм, молоко 1.8% 200 грамм\n\
❌ - гречка с молоком\n\n\
✅ - макароны с мясом индейки: макароны 300 грамм, индейка жаренная 250 грамм\n\
❌ - макароны с индейкой\n\n\
Чем подробнее описание, тем точнее расчет!",
        parse_mode="HTML",
        reply_markup=kb.back
    )
    await state.set_state(Request.user_message)
    

@router_calculation.message(F.text == "Назад")
async def calc(message: Message, state: FSMContext):
    await message.answer(
        text="Главное меню", 
        reply_markup=kb.main
    )
    await state.clear()
    

@router_calculation.message(Request.user_message)    
async def calc(message: Message, state: FSMContext):
    await state.set_state(Request.wait)
    reply = await message.answer(text="Запрос обрабатывается...")
    await message.bot.send_chat_action(
        chat_id=message.from_user.id, 
        action=ChatAction.TYPING
    )
    await state.update_data(user_message=message.text)
    data = await state.get_data()
    
    request = await calc_calories(data["user_message"])
    await state.update_data(request=request)
    if request["warning"] is None:
        await reply.edit_text(
            text=request["nn_answer"],
            reply_markup=kb.calc
        )
    else:
        await reply.edit_text(
            text=request["warning"]
        )
    
    
@router_calculation.message(Request.wait)
async def wait(message: Message):
    await message.answer(
        text="Дождитесь обработки предыдущего запроса..."
    )
    
    
@router_calculation.callback_query(F.data == "add")
async def add(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Добавление в рацион...")
    data = await state.get_data()
    try:
        await rq.set_daily_report(
            callback.from_user.id,
            str(callback.message.date.now(tz=timezone("Europe/Moscow"))),
            data["user_message"],
            data["request"]["CPFC"],
            0
        )
        await rq.user_send_request(
            callback.from_user.id,
            1,
            1,
            data["request"]["usedTokens"],
            0
        )
        await callback.message.answer(
            text="Блюдо успешно добавлено в дневной рацион ✅",
            reply_markup=kb.main
        )
    except Exception as e:
        print(e)
        await callback.message.answer(
            text="Не удалось добавить блюдо в дневной рацион ❌",
            reply_markup=kb.main
        )
        
    await state.clear()
