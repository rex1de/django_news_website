import telebot
from telebot import types 
import os
import django
from slugify import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')
django.setup()

from social_django.models import UserSocialAuth
from main.models import News
from main.models import Category

class Post:
    def __init__(self, user_id=None, title=None, category=None, text=None, description=None, image=None):
        self.user_id = user_id
        self.title = title
        self.category = category
        self.text = text
        self.description = description
        self.image = image

    def publish_post(self):
        self.slug = slugify(self.title)
        category = Category.objects.get(name=self.category)
        news = News(title=self.title, text=self.text, category=category, description=self.description, image=self.image, slug=self.slug)
        news.save()

API_TOKEN = '6478915421:AAHZH_Zxp49blHcsl7bRga0WaxOQotNn-V4'

bot = telebot.TeleBot(API_TOKEN)

def send_news_details(news_details):
    bot.send_message('-4004087466', f"Опубликована новая новость\n{news_details['title']}\n{news_details['description']}\n{news_details['category']}")

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
    bot.reply_to(message, "Главное меню. Выберите действие на клавиатуре", reply_markup=markup) 

@bot.message_handler(func=lambda message: message.text=='Мой профиль')
def profile_keyboard(message):
    user_id = message.chat.id
    user = UserSocialAuth.objects.get(provider='telegram', uid=user_id).user
    bot.send_message(message.chat.id, 
                     f"Профиль\n{user.first_name} {user.last_name}\n{user.username}\nПочта: {user.email}\nДата регистрации: {user.date_joined}\nПоследний онлайн: {user.last_login}\nОставлено комментариев: {len(user.profile.get_user_comments())}\nОпубликовано новостей: {len(user.profile.get_user_news())}")

@bot.message_handler(func=lambda message: message.text=='Создать новость')
def create_post_keyboard(message):
    global post
    global create_post_markup
    post = Post(user_id=message.chat.id)
    create_post_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = [types.KeyboardButton("Заголовок"),
                types.KeyboardButton("Категория"),
                types.KeyboardButton("Краткое описание"),
                types.KeyboardButton("Текст"),
                types.KeyboardButton("Изображение"),
                types.KeyboardButton("Просмотр"),
                types.KeyboardButton("Отправить"),
                types.KeyboardButton("На главную")]
    create_post_markup.add(*buttons)
    bot.send_message(message.chat.id, 'Создание новости', reply_markup=create_post_markup)

@bot.message_handler(func=lambda message: message.text=='Заголовок')
def title(message):
    title_msg = bot.send_message(message.chat.id, 'Введите заголовок новости')
    bot.register_next_step_handler(title_msg, title_validation)

@bot.message_handler(func=lambda message: message.text=='Краткое описание')
def description(message):
    title = bot.send_message(message.chat.id, 'Введите описание новости')
    bot.register_next_step_handler(title, description_validation)

@bot.message_handler(func=lambda message: message.text=='Текст')
def text(message):
    title = bot.send_message(message.chat.id, 'Введите текст новости')
    bot.register_next_step_handler(title, text_validation)

@bot.message_handler(func=lambda message: message.text=='Категория')
def category(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    categories = Category.objects.all()
    buttons = []
    for category in categories:
        buttons.append(types.KeyboardButton(category.name))
    markup.add(*buttons)
    category = bot.send_message(message.chat.id, 'Выберите категорию', reply_markup=markup)
    bot.register_next_step_handler(category, category_selection)

@bot.message_handler(func=lambda message: message.text=='Изображение')
def image(message):
    title = bot.send_message(message.chat.id, 'Выберите изображение')
    bot.register_next_step_handler(title, image_validation)


@bot.message_handler(func=lambda message: message.text=='Отправить')
def send_post(message):
    global post
    if post.title and post.description and post.image and post.text:
        post.publish_post()
        news = News.objects.get(title=post.title)
        bot.send_message(message.chat.id, f'Пост опубликован\nссылка на пост: 127.0.0.1:8000{news.get_absolute_url()}')
    else:
        bot.send_message(message.chat.id, 'Не все поля заполнены!')

@bot.message_handler(func=lambda message: message.text=='Просмотр')
def view_post(message):
    bot.send_message(message.chat.id, f'Заголовок: {post.title}\nкатегория: {post.category}\nописание: {post.description}\nтекст: {post.text}')

@bot.message_handler(func=lambda message: message.text=='На главную')
def to_main_keyboard(message):
    main_keyboard(message)

def category_selection(message):
    global post
    global create_post_markup
    post.category = message.text
    bot.send_message(message.chat.id, 'Категория выбрана', reply_markup=create_post_markup)
    
def text_validation(message):
    global post
    global create_post_markup
    if len(message.text) <= 300:
        text = message.text
        bot.send_message(message.chat.id, 'Текст заполнен', reply_markup=create_post_markup)
    else:
        text = None
        bot.send_message(message.chat.id, 'Длина текста не может быть более 300 символов!', reply_markup=create_post_markup)
    post.text = text

def title_validation(message):
    global post
    global create_post_markup
    if len(message.text) <= 50:
        title = message.text
        bot.send_message(message.chat.id, 'Заголовок заполнен', reply_markup=create_post_markup)
    else:
        title = None
        bot.send_message(message.chat.id, 'Длина заголовка не может быть более 50 символов!', reply_markup=create_post_markup)
    post.title = title

def description_validation(message):
    global post
    global create_post_markup
    if len(message.text) <= 100:
        description = message.text
        bot.send_message(message.chat.id, 'Описание заполнено', reply_markup=create_post_markup)
    else:
        description = None
        bot.send_message(message.chat.id, 'Длина описания не может быть более 100 символов!', reply_markup=create_post_markup)
    post.description = description

def image_validation(message):
    global create_post_markup
    global post
    post.image = message.text
    bot.send_message(message.chat.id, 'Изображение выбрано', reply_markup=create_post_markup)


@bot.message_handler(func=lambda message: message.text=='Подписаться на рассылку')
def subscription_keyboard(message):
    buttons = [[types.InlineKeyboardButton(category.name, callback_data=category.name, url=f'https://t.me/django_news_subscribe_bot?start={category.slug}') for category in Category.objects.all()]]
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