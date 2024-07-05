from functools import partial
import logging
import asyncio
from ssl import SSLContext
from typing import Text
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from psycopg2 import connect
from psycopg2.extras import DictCursor

from database.models import OrderProduct
from restouran import clear_cart


API_TOKEN = '7429950755:AAGxoj2MoGmprbRo-PucZryk90JkQRXiFjI'

# Logging ni sozlash
logging.basicConfig(level=logging.INFO)

# Botni yaratamiz
bot = Bot(token=API_TOKEN)

# Routerni yaratamiz
router = Router()

# PostgreSQL bilan ulanish funksiyasi
def get_db_connection():
    conn = connect(
        dbname='aiogram',
        user='postgres',
        password='Samandar2004',
        host='localhost',
        port='5432'
    )
    return conn

# Mahsulotlar ro'yxatini olish funksiyasi
def fetch_categories():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SELECT name FROM menu")
    categories = cursor.fetchall()
    conn.close()
    return [category['name'] for category in categories]

# Mahsulot ma'lumotlarini olish funksiyasi
def fetch_product_details(product_name):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute("SELECT image, name, description, price FROM menu WHERE name = %s", (product_name,))
    products = cursor.fetchall()
    conn.close()
    return products



# Start komandasi uchun handler
@router.message(Command('start'))
async def send_welcome(message: Message):
    menu_button = KeyboardButton(text='Menu')
    contact_button = KeyboardButton(text='Kontakt')

    keyboard = ReplyKeyboardMarkup(keyboard=[[menu_button, contact_button]], resize_keyboard=True)
    await message.answer("Salom! Nima qilishni xohlaysiz?", reply_markup=keyboard)


# Menu tugmasi uchun handler
@router.message(lambda message: message.text == 'Menu')
async def show_menu(message: Message):
    # Mahsulotlar tugmalarini bazadan olamiz
    products = fetch_categories()

    # Mahsulotlar tugmalarini yaratamiz
    product_buttons = [KeyboardButton(text=product) for product in products]
    back_button = KeyboardButton(text='Orqaga')

    # Klaviatura yaratamiz va tugmalarni qo'shamiz
    keyboard = ReplyKeyboardMarkup(
        keyboard=[product_buttons] + [[back_button]],
        resize_keyboard=True
    )
    # Foydalanuvchiga xabar va klaviaturani jo'natamiz
    await message.answer("Mahsulotlar ro'yxati:", reply_markup=keyboard)


@router.message(lambda message: message.text in fetch_categories())
async def show_product_details(message: Message):
    product_name = message.text
    products = fetch_product_details(product_name)

    if products:
        response_message = f"Name: {products[0]['name']}\nNarxi: {products[0]['price']}\nDescription: {products[0]['description']}"
        if products[0]['image']:
            response_message += f"\n<a href='{products[0]['image']}'>Fayl</a>"
        await message.answer(response_message, parse_mode='HTML')

    await message.answer("Nechta buyurtma qilmoqchisiz? Raqamni kiriting:")
    try:
        quantity = int(message.text)


    except ValueError:
        await message.answer("Iltimos, son kiritishni to'g'ri bajaring.")
    await message.answer(quantity)







# Orqaga tugmasi uchun handler
@router.message(lambda message: message.text == 'Orqaga')
async def go_back(message: Message):
    menu_button = KeyboardButton(text='Menu')
    contact_button = KeyboardButton(text='Kontakt', request_contact=True)
    keyboard = ReplyKeyboardMarkup(keyboard=[[menu_button, contact_button]], resize_keyboard=True)

    # Foydalanuvchiga xabar va klaviaturani jo'natamiz
    await message.answer("Asosiy menyuga qaytdingiz.", reply_markup=keyboard)

async def main():
    # Dispatcher ni yaratamiz
    dp = Dispatcher()

    # Routerni dispatcher ga qo'shamiz
    dp.include_router(router)
    # Botni faqat tugmani bosqichiga olishimiz uchun handlerlarni qo'shamiz




    # Dispatcher yordamida polling ni boshlaymiz
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
