import os
import threading
import requests
from flask import Flask
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

BOT_TOKEN = "8753239454:AAFYP7Wyn1PelCxMnQkIVdsPtxoyAzO91gA"
WEBAPP_URL = "https://incomparable-cupcake-e2fcdb.netlify.app"
IMG_BOT_KEY = "21006dc513d124de285c47b2bddfdee7"
ADMIN_IDS = [8780056363, 8403172681]

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name or "друг"
    text = (
        f"👋 Привет, {name}!\n\n"
        "🛍 Добро пожаловать в <b>STREAD SHOP</b>!\n\n"
        "🔥 У нас огромный выбор:\n"
        "💧 Жидкости\n"
        "💨 Поды\n"
        "📦 Картриджи\n"
        "🌿 Снюс\n"
        "⚡ Никобустеры\n\n"
        "🎁 Промокоды, скидки и быстрый заказ — всё внутри приложения.\n\n"
        "👇 <b>Жми кнопку ниже, чтобы открыть магазин!</b>"
    )
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text="🛍 Открыть магазин",
        web_app=WebAppInfo(url=WEBAPP_URL)
    ))
    bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "❌ Нет доступа")
        return
    bot.reply_to(message, "⏳ Загружаю фото...")
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded = bot.download_file(file_info.file_path)
        files = {'image': downloaded}
        r = requests.post('https://api.imgbb.com/1/upload?key=' + IMG_BOT_KEY, files=files)
        data = r.json()
        if data.get('success'):
            url = data['data']['url']
            bot.reply_to(
                message,
                "✅ Ссылка на фото:\n`" + url + "`\n\nСкопируйте и вставьте в админке.",
                parse_mode="Markdown"
            )
        else:
            bot.reply_to(message, "❌ Ошибка загрузки")
    except Exception as e:
        bot.reply_to(message, "❌ Ошибка: " + str(e))

@bot.message_handler(func=lambda m: True)
def any_msg(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(
        text="🛍 Открыть магазин",
        web_app=WebAppInfo(url=WEBAPP_URL)
    ))
    bot.send_message(message.chat.id, "Нажми кнопку ниже 👇", reply_markup=markup)

def run_bot():
    bot.infinity_polling()

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running"

@app.route('/health')
def health():
    return "OK", 200

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
