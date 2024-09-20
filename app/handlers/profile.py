from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.states import User
import app.database.requests as rq
from app.calculations.calc_standard import calc_standard


router_profile = Router()


# Профиль
@router_profile.message(F.text == "Профиль")
async def profile(message: Message):
    user_data = [data for data in await rq.get_user_data(message.from_user.id)][0]
    
    text = f"<strong>Имя:</strong> {message.from_user.first_name}\n\
<strong>ID:</strong> {message.from_user.id}\n\n\
<strong>Пол:</strong> {user_data.gender if user_data.gender else '-'}\n\
<strong>Возраст:</strong> {user_data.age if user_data.age else '-'}\n\
<strong>Рост:</strong> {user_data.height if user_data.height else '-'} см\n\
<strong>Вес:</strong> {user_data.weight if user_data.weight else '-'} кг\n\n\
<strong>Образ жизни:</strong> {user_data.lifestyle if user_data.lifestyle else '-'}\n\
<strong>Цель:</strong> {user_data.goal if user_data.goal else '-'}\n\n\
<strong>Суточная норма КБЖУ:</strong>\n\
<blockquote>Калории: {user_data.standard['standard']['calories']}\n\
Белки: {user_data.standard['standard']['proteins']}\n\
Жиры: {user_data.standard['standard']['fats']}\n\
Углеводы: {user_data.standard['standard']['carbohydrates']}</blockquote>"
        
    await message.answer(
        text=text,
        parse_mode="HTML",
        reply_markup=kb.profile
    )

 
# Редактирование профиля   
@router_profile.callback_query(F.data == "edit")
async def edit_profile(callback: CallbackQuery, state: FSMContext):
    await callback.answer(
        text="Изменение данных профиля"
    )
    await callback.message.answer(
        text="Ваш пол:",
        reply_markup=kb.gender
    )
    await state.set_state(User.gender)
    

@router_profile.message(User.gender)
async def user_age(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await state.set_state(User.age)
    await message.answer("Введите Ваш возраст:")
    
    
@router_profile.message(User.age)
async def user_height(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(User.height)
    await message.answer("Введите Ваш рост (см):") 
    
    
@router_profile.message(User.height)
async def user_weight(message: Message, state: FSMContext):
    await state.update_data(height=message.text)
    await state.set_state(User.weight)
    await message.answer("Введите Ваш вес (кг):")
    
    
@router_profile.message(User.weight)
async def user_lifestyle(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await state.set_state(User.lifestyle)
    await message.answer("Ваш образ жизни:", reply_markup=kb.lifestyle)
    
    
@router_profile.message(User.lifestyle)
async def user_purpose(message: Message, state: FSMContext):
    await state.update_data(lifestyle=message.text)
    await state.set_state(User.goal)
    await message.answer("Ваша цель:", reply_markup=kb.goal)
    

@router_profile.message(User.goal)
async def total(message: Message, state: FSMContext):
    await state.update_data(goal=message.text)
    data = await state.get_data()
    standard = await calc_standard(
        data["gender"], 
        int(data["age"]), 
        int(data["height"]), 
        int(data["weight"]), 
        data["lifestyle"], 
        data["goal"]
    )
    try:
        await rq.update_user_data(
            message.from_user.id, 
            data["gender"], 
            int(data["age"]),
            int(data["height"]),
            int(data["weight"]),
            data["lifestyle"],
            data["goal"],
            standard
        )
        await message.answer(
            text=f"Данные успешно сохранены в Ваш профиль ✅",
            reply_markup=kb.main
        )
        await state.clear()
    except:
        await message.answer(
            text="Не удалось сохранить Ваши данные, проверьте правильность введенных данных и попробуйте еще ❌"
        )
        await state.clear()
    

# Дневник питания
@router_profile.callback_query(F.data == "report") 
async def report(callback: CallbackQuery):
    await callback.answer("Дневной рацион...")
    reports = [data for data in await rq.get_daily_report(callback.from_user.id, str(callback.message.date)[:10])]
    final_report = {
        "calories": 0,
        "proteins": 0,
        "fats": 0,
        "carbohydrates": 0
    }
    try:
        for i in range(len(reports)):
            final_report["calories"] += reports[i].dailyReport["calories"]
            final_report["proteins"] += reports[i].dailyReport["proteins"]
            final_report["fats"] += reports[i].dailyReport["fats"]
            final_report["carbohydrates"] += reports[i].dailyReport["carbohydrates"]
            
            await callback.message.answer(
                text=f"<strong>{reports[i].mealDescription}:</strong>\n\
<blockquote><strong>Калории:</strong> {reports[i].dailyReport['calories']}\n\
<strong>Белки:</strong> {reports[i].dailyReport['proteins']}\n\
<strong>Жиры:</strong> {reports[i].dailyReport['fats']}\n\
<strong>Углеводы:</strong> {reports[i].dailyReport['carbohydrates']}</blockquote>",
                reply_markup=kb.delete,
                parse_mode="HTML"
            )
        await callback.message.answer(
            text=f"<strong>Общее количество калорий и БЖУ:</strong>\n\
<blockquote><strong>Калории:</strong> {final_report['calories']}\n\
<strong>Белки:</strong> {final_report['proteins']}\n\
<strong>Жиры:</strong> {final_report['fats']}\n\
<strong>Углеводы:</strong> {final_report['carbohydrates']}</blockquote>",
            parse_mode="HTML"
        )
    except:
        await callback.message.answer(
            text="Вы еще не добавили ни одной записи!"
        )

        
@router_profile.callback_query(F.data == "delete")
async def delete(callback: CallbackQuery):
    await callback.answer("Удаление...")
    try:
        await rq.delete_daily_report(
            callback.from_user.id, 
            callback.message.text[:callback.message.text.find(":")]
        )
        await callback.message.answer(
            text="Прием пищи успешно удален ✅"
            )
    except:
        await callback.message.answer(
            text="Не удалось удалить прием пищи ❌"
        )
