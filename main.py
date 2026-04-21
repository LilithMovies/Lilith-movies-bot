import telebot
from pymongo import MongoClient

# MongoDB Connection String (မိတ်ဆွေ Copy ကူးလာတဲ့ လင့်ခ်ကို ဒီမှာ ထည့်ပါ)
# <password> နေရာမှာ password အစစ် ပြောင်းဖို့ မမေ့ပါနဲ့
MONGO_URL = "mongodb+srv://LilithSY:Lilith2004@cluster0.mrqj6fl.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URL)
db = client['bot_database']
collection = db['videos']

# ကိုယ့်ရဲ့ Bot Token ကို ဒီမှာ ထည့်ပါ
API_TOKEN = 'ကိုယ့်_Bot_Token_ဒီမှာ_ထည့်ပါ'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(content_types=['video'])
def handle_video(message):
    file_id = message.video.file_id
    
    # Database ထဲမှာ ဗီဒီယိုကို နံပါတ်စဉ်တပ်ပြီး သိမ်းခြင်း
    v_count = collection.count_documents({})
    v_id = str(v_count + 1)
    
    collection.insert_one({"v_id": v_id, "file_id": file_id})
    
    bot_info = bot.get_me()
    link = f"https://t.me/{bot_info.username}?start={v_id}"
    bot.reply_to(message, f"✅ Database ထဲမှာ အမြဲတမ်းအတွက် သိမ်းလိုက်ပါပြီ!\n\nဒီ Link ကို Channel မှာ သုံးလို့ရပါပြီ - {link}")

@bot.message_handler(commands=['start'])
def start_and_send(message):
    text = message.text.split()
    if len(text) > 1:
        v_id = text[1]
        # Database ထဲမှာ ပြန်ရှာခြင်း
        data = collection.find_one({"v_id": v_id})
        if data:
            bot.send_video(message.chat.id, data['file_id'], caption="🎬 ကြည့်ရှုအားပေးမှုကို ကျေးဇူးတင်ပါသည်။")
        else:
            bot.send_message(message.chat.id, "❌ စိတ်မရှိပါနဲ့၊ ဒီဗီဒီယိုကို ရှာမတွေ့တော့ပါဘူး။")
    else:
        bot.send_message(message.chat.id, "မင်္ဂလာပါ၊ Bot ကို စတင်အသုံးပြုဖို့ Channel က လင့်ခ်တွေကတစ်ဆင့် ဝင်ရောက်ပေးပါ။")

if __name__ == "__main__":
    bot.infinity_polling()
