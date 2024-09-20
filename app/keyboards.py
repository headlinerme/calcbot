from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Расчет КБЖУ")
        ],
        [
            KeyboardButton(text="Профиль"), 
            KeyboardButton(text="Техподдержка")
        ]
    ],
    resize_keyboard=True
)

calc = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Добавить в рацион", callback_data="add")]
    ]
)

back = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Назад")]
    ],
    resize_keyboard=True
)

profile = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Токены", callback_data="requests")],
        [InlineKeyboardButton(text="Изменить данные", callback_data="edit")],
        [InlineKeyboardButton(text="Дневной рацион", callback_data="report")]
    ]
)

delete = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Удалить", callback_data="delete")]
    ]
)

gender = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Мужчина"), 
            KeyboardButton(text="Женщина")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

lifestyle = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Малоподвижный образ жизни"),
            KeyboardButton(text="Тренировки 1-3 раза в неделю"),
        ],
        [
            KeyboardButton(text="Тренировки 3-5 раз в неделю"),
            KeyboardButton(text="Высокие нагрузки каждый день"),
        ],
        [
            KeyboardButton(text="Экстремальные нагрузки")
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

goal = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Потеря жира"), 
            KeyboardButton(text="Рекомпозиция")
        ],
        [
            KeyboardButton(text="Набор массы"),
            KeyboardButton(text="Поддержание веса"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)
