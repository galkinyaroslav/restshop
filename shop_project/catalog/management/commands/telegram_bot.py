from aiogram import Bot, Dispatcher, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from django.core.management.base import BaseCommand
from django.conf import settings
from asgiref.sync import sync_to_async
from catalog.models import Category, Producer
import json
import requests

bot = Bot(token=settings.TELEGRAM_API_KEY)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                               one_time_keyboard=False)
button_categories = KeyboardButton('Categories')
button_producers = KeyboardButton('Producers')
button_cart = KeyboardButton('Show User Cart')
keyboard.add(button_categories)
keyboard.add(button_producers)
keyboard.add(button_cart)


class SomeState(StatesGroup):
    waiting_for_text = State()


@sync_to_async()
def get_categories():
    return list(Category.objects.all())


@sync_to_async()
def get_producers():
    return list(Producer.objects.all())


@dp.message_handler(lambda message: message.text == 'Categories')
async def show_categories(message: types.Message):
    msg_to_answer = ''
    categories = await get_categories()
    for category in categories:
        msg_to_answer += f'Category: {category.name}\n' \
                         f'Description: {category.description}\n'
    await bot.send_message(message.chat.id, msg_to_answer)


@dp.message_handler(lambda message: message.text == 'Producers')
async def show_producers(message: types.Message):
    msg_to_answer = ''
    producers = await get_producers()
    for producer in producers:
        msg_to_answer += f'Producer: {producer.name}\n' \
                         f'Country: {producer.description}\n'
    await bot.send_message(message.chat.id, msg_to_answer)


@dp.message_handler(commands=['help', 'start'])
async def command_helper(message: types.Message):
    await message.answer('Input some message', reply_markup=keyboard)


@dp.message_handler(Text('Show User Cart'))
async def ask_for_credentials(message: types.Message):
    await message.reply('Enter Login and password divided by "," (Ex. login,password)')
    await SomeState.waiting_for_text.set()


@dp.message_handler(state=SomeState.waiting_for_text)
async def show_user_cart(message: types.Message, state: FSMContext):
    msg_text = message.text
    login, password = msg_text.split(',')
    data = {
        "email": login,
        "password": password
    }

    response = requests.post("http://127.0.0.1:8000/users/auth/jwt/create/",
                             data=json.dumps(data),
                             headers={
                                 "Content-Type": "application/json"
                             })
    print(response)
    if response.status_code == 200:
        token = json.loads(response.content)['access']
        response = requests.get('http://127.0.0.1:8000/api/catalog/cart/',
                                headers={
                                    "Authorization": f"Bearer {token}"
                                })
        user_cart_data = json.loads(response.content)
        if user_cart_data:
            msg_to_answer = ''
            products = user_cart_data['products']
            for prod in products:
                msg_to_answer += f"Product: {prod['name']}, number of items: {prod['number_of_items']}\n"
            msg_to_answer += f"Result price: {user_cart_data['result_price']}"
            await bot.send_message(message.chat.id, msg_to_answer)
        else:
            await bot.send_message(message.chat.id, 'Empty cart')
    await state.finish()

@dp.message_handler()
async def query_telegram(message: types.Message):
    await bot.send_message(message.chat.id, 'Understandable, have a nice day')


class Command(BaseCommand):
    help = 'Test TG Bot'

    def handle(self, *args, **options):
        executor.start_polling(dp)
