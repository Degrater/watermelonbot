from aiogram.dispatcher.filters.state import StatesGroup,State
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton , ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

storage = MemoryStorage()
api_Token = "5741446133:AAHXwLWGyQwCKWdA6asJCKogrM0Ul1g89Bw"
bot = Bot(token=api_Token)
dp = Dispatcher(bot,storage=storage)

button_menu = ReplyKeyboardMarkup(resize_keyboard=True, selective=True, row_width=3).add(KeyboardButton("Меню"),
                                                                                        KeyboardButton("Корзина"),
                                                                                        KeyboardButton("Помощь"),
                                                                                        KeyboardButton("О нас"))
    
kb_menu = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton("Романза" ,  callback_data="romanza"),
                                                InlineKeyboardButton("Топ Ган",callback_data="top_gun"),
                                                InlineKeyboardButton("Назад",callback_data="start"))


class UserState(StatesGroup):
    amount0 = State()
    amount1 = State()

@dp.message_handler(commands=['start','help'])
async def send_welcome(message: types.Message,state=None):
    await message.reply("Добро пожаловать в наш телеграмм магазин!\nМы выращиваем только натуральные фрукты и овощи. ", reply_markup=button_menu)

@dp.message_handler(lambda message: message.text =="Меню")
async def menu_answer(message: types.Message,state=None):
    await message.answer("Сорт:", reply_markup = kb_menu)

@dp.callback_query_handler(lambda c: c.data == "romanza")
async def amount_romanza(callback_query: types.CallbackQuery, state=None):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите количество арбузов:")
    await UserState.amount0.set()

@dp.message_handler(state=UserState.amount0)
async def get_am0(message: types.Message, state: FSMContext):
    await state.update_data(amount0=message.text)
    await message.answer("Отлично , введите вес арбузов :")
    await UserState.amount1.set()

@dp.message_handler(state=UserState.amount1)
async def get_am1(message: types.Message, state: FSMContext):
    await state.update_data(amount1=message.text)
    data = await state.get_data()
    await message.answer(f"Количество: {data['amount0']} , Килограммы : {data['amount1']} ")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)
