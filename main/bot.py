import telebot

API_TOKEN = '6028563550:AAEp4u3Y5AvX56c4lMIxwWa3raNw3eZUsZE'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Привет!\nЯ бот который умеет взаимодействовать с новостным сайтом")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
def send_news_details(news_details):
    bot.send_photo('-4004087466', news_details['image'], f'''Опубликована новая новость\n{news_details['title']}\n{news_details['description']}\n{news_details['category']}''')
    
bot.polling()