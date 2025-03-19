import logging
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import ReplyKeyboardMarkup, WebAppInfo, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.enums import ParseMode
from database import save_user, get_user

def url_maker(token):
    web_app_url = f"https://trendmax-shop-online.netlify.app?token={token}"
    return web_app_url

# 🔹 Bot Token


async def update_user_info(telegram_id, first_name):
    user = get_user(telegram_id)
    if user:
        token = user[2]
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"first_name": first_name}
        
        async with aiohttp.ClientSession() as session:
            async with session.patch(UPDATE_URL, json=payload, headers=headers) as response:
                if response.status == 200:
                    return True
    return False

async def refresh_token(telegram_id):
    user = get_user(telegram_id)
    if user:
        phone = user[1]
        payload = {"phone": phone, "telegram_id": telegram_id, "first_name": "User"}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(LOGIN_URL, json=payload) as response:
                data = await response.json()
                if response.status == 200 and "data" in data:
                    new_token = data["data"]["token"]
                    save_user(telegram_id, phone, new_token)  # Yangi tokenni saqlash
                    return new_token
    return None
command_router = Router()
API_TOKEN = "8044225277:AAHomznJqD6JHyfcvIG1j1uJj8SGl3FATQQ"
LOGIN_URL = "https://dev.api.gosslujba.dynamicsoft.uz/api/users/login"
UPDATE_URL = "https://dev.api.gosslujba.dynamicsoft.uz/api/users/update"

# 🔹 Logger
logging.basicConfig(level=logging.INFO)

# 🔹 Bot va Dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# 🔹 Telefon yuborish tugmasi
phone_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)
    ]
], resize_keyboard=True, one_time_keyboard=True)

# 🔹 /start komandasi
@command_router.message(Command("start"))
async def send_welcome(message: types.Message):
    telegram_id = message.from_user.id
    user = get_user(telegram_id)  # Bazadan foydalanuvchini olish

    if user:
        # Foydalanuvchi allaqachon ro'yxatdan o'tgan
        token = user[3]  # Token bazadan olinadi
        print(token)
        await message.answer(
            f"👕👗 *Assalomu alaykum, hurmatli mijoz!* 😊\n\n"
            f"✨ *Eng so‘nggi trenddagi kiyim-kechaklar* bizning botimizda! "
            f"Yuqori sifatli, zamonaviy va qulay mahsulotlar endi bir necha tugma bosish orqali qo‘lingizda! 🛍️\n\n"
            f"🔥 *Stil va qulaylikni bir joyda toping!*\n"
            f"🛒 *Harid qilish uchun quyidagi tugmani bosing!* 👇",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="🛍️ HARID QILISH", web_app=WebAppInfo(url=url_maker(token=token)))
                ]
            ])
        )
    else:
        # Foydalanuvchi ro'yxatdan o'tmagan
        await message.answer("Salom! Ro‘yxatdan o‘tish uchun telefon raqamingizni yuboring.", reply_markup=phone_keyboard)

# 🔹 Telefon raqamini qabul qilish
@command_router.message(lambda message: message.contact)
async def register_user(message: types.Message):
    phone = message.contact.phone_number
    telegram_id = message.from_user.id

    payload = {"phone": phone, "telegram_id": telegram_id, "first_name": message.from_user.first_name}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(LOGIN_URL, json=payload) as response:
            data = await response.json()
            if response.status == 200 and "data" in data:
                token = data["data"]["token"]
                await update_user_info(telegram_id, message.from_user.first_name)  # Foydalanuvchi ma'lumotlarini yangilash
                save_user(telegram_id, phone, token)  # Ma'lumotlar bazasiga saqlash

                await message.answer(f"✅ Ro‘yxatdan o‘tish muvaffaqiyatli!\n", reply_markup=ReplyKeyboardRemove())
                await message.answer(
                    f"👕👗 *Assalomu alaykum, hurmatli mijoz!* 😊\n\n"
                    f"✨ *Eng so‘nggi trenddagi kiyim-kechaklar* bizning botimizda! "
                    f"Yuqori sifatli, zamonaviy va qulay mahsulotlar endi bir necha tugma bosish orqali qo‘lingizda! 🛍️\n\n"
                    f"🔥 *Stil va qulaylikni bir joyda toping!*\n"
                    f"🛒 *Harid qilish uchun quyidagi tugmani bosing!* 👇",
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [
                            InlineKeyboardButton(text="🛍️ HARID QILISH", web_app=WebAppInfo(url=url_maker(token=token)))
                        ]
                    ])
                )

            else:
                await message.answer("❌ Ro‘yxatdan o‘tishda xatolik yuz berdi. Iltimos, qayta urinib ko‘ring.")

# 🔹 Botni ishga tushirish
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(command_router)  # Router qo'shish
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())