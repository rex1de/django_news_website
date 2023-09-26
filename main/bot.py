import telebot
from telebot import types 
API_TOKEN = '6478915421:AAHZH_Zxp49blHcsl7bRga0WaxOQotNn-V4'

bot = telebot.TeleBot(API_TOKEN)

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
def send_news_details(news_details):
    bot.send_message('-4004087466', f'''Опубликована новая новость\n{news_details['title']}\n{news_details['description']}\n{news_details['category']}''')

# def send_news_details(news_details):
#     bot.send_photo('-4004087466', news_details['image'], f'''Опубликована новая новость\n{news_details['title']}\n{news_details['description']}\n{news_details['category']}''')    

@bot.message_handler(commands=['start'])
def login_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Войти в аккаунт")
    markup.add(button1)
    bot.reply_to(message, "Привет!\nЯ бот который умеет взаимодействовать с новостным сайтом\nВыбери действие на клавиатуре", reply_markup=markup) 

@bot.message_handler(func=lambda message: message.text=='Войти в аккаунт')
def main_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton("Мой профиль"),
                types.KeyboardButton("Создать новость"),
                types.KeyboardButton("Подписаться на рассылку")]
    markup.add(*buttons)
    bot.reply_to(message, "Вы успешно вошли в аккаунт. Выберите действие на клавиатуре", reply_markup=markup) 

@bot.message_handler(func=lambda message: message.text=='Мой профиль')
def profile_keyboard(message):
    bot.send_message(message.chat.id, "Профиль")

@bot.message_handler(func=lambda message: message.text=='Создать новость')
def create_post_keyboard(message):
    bot.send_message(message.chat.id, 'Создать новость')

@bot.message_handler(func=lambda message: message.text=='Подписаться на рассылку')
def subscription_keyboard(message):
    global subscription_markup
    buttons = [[types.InlineKeyboardButton("Спорт", callback_data='Спорт', url='https://t.me/django_news_subscribe_bot?start=sport' ),
                types.InlineKeyboardButton("Политика", callback_data='Политика', url='https://t.me/django_news_subscribe_bot?start=politics'),
                types.InlineKeyboardButton("Кино", callback_data='Кино', url='https://t.me/django_news_subscribe_bot?start=kino'),
                types.InlineKeyboardButton("Бизнес", callback_data='Бизнес', url='https://t.me/django_news_subscribe_bot?start=biznes')]]
    subscription_markup = types.InlineKeyboardMarkup(buttons, row_width=4)
    bot.reply_to(message, "Выберите ниже желаемые категории", reply_markup=subscription_markup) 

# @bot.message_handler(func=lambda message: message.text=='Подписаться на рассылку')
# def subscription_keyboard(message):
#     global subscription_markup
#     buttons = [[types.InlineKeyboardButton("Спорт", callback_data='Спорт'),
#                 types.InlineKeyboardButton("Политика", callback_data='Политика'),
#                 types.InlineKeyboardButton("Кино", callback_data='Кино'),
#                 types.InlineKeyboardButton("Бизнес", callback_data='Бизнес')],
#                 [types.InlineKeyboardButton("Подписаться на рассылку", callback_data='Подписка', url='https://t.me/django_news_subscribe_bot')]]
#     subscription_markup = types.InlineKeyboardMarkup(buttons, row_width=4)
#     bot.reply_to(message, "Выберите ниже желаемые категории", reply_markup=subscription_markup) 

# @bot.callback_query_handler(func=lambda call: True)
# def inline_callback(call):
#     if call.message:
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'{call.message.text}\n{call.data} ✅', reply_markup=subscription_markup)

if __name__ == '__main__':
    bot.polling()

