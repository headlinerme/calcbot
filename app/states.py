from aiogram.fsm.state import StatesGroup, State


class User(StatesGroup):
    gender = State()
    age = State()
    height = State()
    weight = State()
    lifestyle = State()
    goal = State()


class Request(StatesGroup):
    user_message = State()
    request = State()
    wait = State()
