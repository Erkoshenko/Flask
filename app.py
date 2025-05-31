import telebot

BOT_TOKEN = "8175491637:AAF_-6-4EeUN-hkvhcdhmdQ9RdpmDGrts8s"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hi!')

bot.polling(none_stop=True)
