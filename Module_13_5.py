from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio


api = ";-)"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb = ReplyKeyboardMarkup(resize_keyboard = True)
button1 = KeyboardButton(text = "Информация")
button2 = KeyboardButton(text = "Рассчитать")
kb.row(button1, button2)

class UserState(StatesGroup, option = None):
    age = State()
    growth = State()
    weight = State()
    gender = State()

@dp.message_handler(commands = ["start"])
async def start(message):
    await message.answer("Приветствую тебя в нашем боте!", reply_markup = kb)

@dp.message_handler(text = "Информация")
async def inform(message):
    await message.answer("Информация о боте:\n"
                         "Бот оказывает помощь твоему здоровью. \n"
                         "Производит вычисление суточного потребления калорий по формуле Миффлина-Сан Жеора")


@dp.message_handler(text = "Рассчитать")
async def set_age(message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer("Введите свой рост (в см.):")
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer("Введите свой вес (в кг.):")
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def set_gender(message, state):
    await state.update_data(weight = message.text)
    await message.answer("Введите свой пол (М , Ж):")
    await UserState.gender.set()

@dp.message_handler(state = UserState.gender)
async def send_calories(message, state):
    await state.update_data(gender = message.text)
    data = await state.get_data()
    try:
        if data['gender'] == 'М':
            calor = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
        elif data['gender'] == 'Ж':
            calor = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) - 161
        await message.answer(f'Ваша норма калорий в сутки: {calor}')
    except (ValueError, UnboundLocalError):
        await message.answer("Введены не корректные данные")
    await state.finish()

@dp.message_handler()
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
