import telebot
from pymongo import MongoClient
import os
from flask import Flask
from threading import Thread

# ၁။ Render Error မတက်အောင် Port ဖွင့်ပေးခြင်း (Keep Alive)
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

def keep_alive():
    t = Thread(target=run)
    t.start()

# ၂။ MongoDB ချိတ်ဆက်ခြင်း
# <password> နေရာမှာ ကိုယ့် password အစစ် ပြောင်းပါ
MONGO_URL = "mongodb+srv://LilithSY:Lilith2004@cluster0.mrqj6fl.mongodb.net/?appName=Cluster0"
client = MongoClient(MONGO_URL)
db = client['bot_database']
collection = db['videos']

# ၃။ Telegram Bot သတ်မှတ်ခြင်း
API_TOKEN = 'မိတ်ဆွေရဲ့_Bot_Token_ကို_ဒီမှာ_အစားထိုးပါ'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    file_id = message.video.file_id
    v_count = collection.count_documents({})
    v_id = str(v_count + 1)
    collection.insert_one({"v_id": v_id, "file_id": file_id})
    
    bot_info = bot.get_me()
    link = f"https://t.me/{bot_info.username}?start={v_id}"
    bot.reply_to(message, f"✅ Database ထဲ သိမ်းပြီးပါပြီ!\n\nLink - {link}")

@bot.message_handler(commands=['start'])
def start_and_send(message):
    text = message.text.split()
    if len(text) > 1:
        v_id = text[1]
        data = collection.find_one({"v_id": v_id})
        if data:
            bot.send_video(message.chat.id, data['file_id'], caption="🎬 ကြည့်ရှုအားပေးမှုကို ကျေးဇူးတင်ပါသည်။")
        else:
            bot.send_message(message.chat.id, "❌ ဇာတ်ကားရှာမတွေ့ပါ။")
    else:
        bot.send_message(message.chat.id, "မင်္ဂလာပါ၊ Channel လင့်ကနေတစ်ဆင့် ဝင်ရောက်ပေးပါ။")

if __name__ == "__main__":
    keep_alive() # Port ကို စတင်နှိုးခြင်း
    bot.infinity_polling()
