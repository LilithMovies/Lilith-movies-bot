import telebot
import os

# Token ကို ဒီမှာ သေချာထည့်ပါ
API_TOKEN = '8395497642:AAEaRUKBxz05Ywyuf4vTEMBvLBYncEba8gU'
bot = telebot.TeleBot(API_TOKEN)

video_db = {}

@bot.message_handler(content_types=['video'])
def handle_video(message):
    try:
        file_id = message.video.file_id
        v_id = str(len(video_db) + 1)
        video_db[v_id] = file_id
        bot_info = bot.get_me()
        link = f"https://t.me/{bot_info.username}?start={v_id}"
        bot.reply_to(message, f"✅ သိမ်းဆည်းပြီးပါပြီ!\n\nLink - {link}")
    except: pass

@bot.message_handler(commands=['start'])
def start_and_send(message):
    text = message.text.split()
    if len(text) > 1:
        v_id = text[1]
        if v_id in video_db:
            bot.send_video(message.chat.id, video_db[v_id], caption="🎬 ကြည့်ရှုအားပေးမှုကို ကျေးဇူးတင်ပါသည်။")
        else:
            bot.send_message(message.chat.id, "❌ ဇာတ်ကားရှာမတွေ့ပါ။")
    else:
        bot.send_message(message.chat.id, "မင်္ဂလာပါ၊ Channel လင့်ကနေတစ်ဆင့် ဝင်ရောက်ပေးပါ။")

if __name__ == "__main__":
    bot.infinity_polling()
