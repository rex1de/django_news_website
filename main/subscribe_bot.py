import telebot

API_TOKEN = '6352958349:AAEO9_So9Zg3bFQD4H3vcToEfeyslFzFqDU'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def subscribe_user(message):
    category = message.text.split()[1] if len(message.text.split()) > 1 else None
    user_id = message.from_user.id
    if category == 'kino':
        bot.reply_to(message, "Вы подписались на новости кино") 
    elif category == 'biznes':
        bot.reply_to(message, "Вы подписались на новости бизнеса") 
    elif category == 'politics':
        bot.reply_to(message, "Вы подписались на новости политики") 
    elif category == 'sport':   
        bot.reply_to(message, "Вы подписались на новости спорта") 
    else:
        bot.reply_to(message, f"Привет!\nЯ бот рассылки. Для того чтобы подписаться на рассылку нужно обязательно перейти по ссылке из основного бота.") 

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
def send_to_subscribers(news_details, telegram_ids):
    for id in telegram_ids:
        bot.send_message(id, f'''Опубликована новая новость в категории {news_details['category']}\n{news_details['title']}\n{news_details['description']}''')


def created_post(news_details):
    bot.send_message('@django_news_channel', f'''{news_details['title']}\n#{news_details['category']}\n{news_details['description']}\n\n\n<a href="127.0.0.1:8000{news_details['url']}">Перейти к новости</a>''', parse_mode='HTML')

# def send_news_details(news_details):
#     bot.send_photo('-4004087466', news_details['image'], f'''Опубликована новая новость\n{news_details['title']}\n{news_details['description']}\n{news_details['category']}''')
    

if __name__ == '__main__':
    bot.polling()

