import logging
import asyncio
import os
import psycopg2
from aiogram import Bot, Dispatcher, types

logging.basicConfig(level=logging.INFO)

# Temporarily set the bot token directly for debugging
os.environ['BOT_TOKEN'] = '7429950755:AAGxoj2MoGmprbRo-PucZryk90JkQRXiFjI'

# Retrieve the bot token from environment variable
bot_token = os.getenv('BOT_TOKEN')

if not bot_token:
    raise ValueError("No bot token provided. Please set the BOT_TOKEN environment variable.")

bot = Bot(token=bot_token)
dp = Dispatcher(bot=bot)

# Logging Middleware
class LoggingMiddleware:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def on_process_message(self, message: types.Message, data: dict):
        self.logger.info(f"Received message: {message.text}")

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        self.logger.info(f"Received callback query: {call.data}")

dp.middleware.setup(LoggingMiddleware())

# PostgreSQL bilan ulanish funksiyasi
def get_db_connection():
    conn = psycopg2.connect(
        dbname='aiogram',
        user='postgres',
        password='Samandar2004',
        host='localhost',
        port='5432'
    )
    return conn

# Start xabari
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Menu", "Delivery", "Contact", "Book a Table", "Comments")
    await message.answer("Salom pitsa restoraniga hush kelibsiz!", reply_markup=markup)

# Menu ko'rsatish
@dp.message_handler(lambda message: message.text == "Menu")
async def show_menu(message: types.Message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM menu')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    
    markup = types.InlineKeyboardMarkup()
    for item in items:
        markup.add(types.InlineKeyboardButton(item[0], callback_data=item[0]))
    await message.answer("Select an item:", reply_markup=markup)

# Taom tafsilotlarini ko'rsatish
@dp.callback_query_handler(lambda c: True)
async def show_item(call: types.CallbackQuery):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM menu WHERE name = %s', (call.data,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if item:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Add to Cart", callback_data=f"add_{item[1]}"))
        await bot.send_photo(call.message.chat.id, item[2], 
                             caption=f"{item[1]}\n\n{item[3]}\nPrice: {item[4]} UZS", 
                             reply_markup=markup)
    else:
        await call.answer("Item not found!")

# Savatga qo'shish
cart = {}

@dp.callback_query_handler(lambda c: c.data.startswith('add_'))
async def add_to_cart(call: types.CallbackQuery):
    item_name = call.data[4:]
    if item_name in cart:
        cart[item_name] += 1
    else:
        cart[item_name] = 1
    await call.answer(f"{item_name} added to cart!")

# Savatni ko'rsatish
@dp.message_handler(lambda message: message.text == "Cart")
async def show_cart(message: types.Message):
    if not cart:
        await message.answer("Your cart is empty.")
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM menu')
        items = cursor.fetchall()
        cursor.close()
        conn.close()
        
        text = ""
        total = 0
        for item_name, quantity in cart.items():
            for item in items:
                if item[1] == item_name:
                    text += f"{item_name}: {quantity} x {item[4]} UZS\n"
                    total += quantity * item[4]
                    break
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Clear Cart", callback_data="clear_cart"))
        await message.answer(f"Your cart:\n\n{text}\n\nTotal: {total} UZS", reply_markup=markup)

# Savatni tozalash
@dp.callback_query_handler(lambda c: c.data == "clear_cart")
async def clear_cart(call: types.CallbackQuery):
    cart.clear()
    await call.answer("Cart cleared!")
    await call.message.answer("Your cart is empty now.")

# Asyncio yordamida botni ishga tushirish
async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
