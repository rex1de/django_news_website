import telebot, os, django

API_TOKEN = '6352958349:AAEO9_So9Zg3bFQD4H3vcToEfeyslFzFqDU'

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')
# django.setup()

from social_django.models import UserSocialAuth
from main.models import Category

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def subscribe_user(message):
    user_id = message.chat.id
    user = UserSocialAuth.objects.get(provider='telegram', uid=user_id).user
    category_slug = message.text.split()[1] if len(message.text.split()) > 1 else None
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        user.profile.subscription_categories.add(category)
        bot.reply_to(message, f"Вы подписались на {category.name}")
    else:
        bot.send_mesage(user_id, 'Привет! Я бот рассылки\nЧтобы подписаться на рассылку нужно обязательно перейти по ссылке из основного бота')


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
def send_to_subscribers(news_details, telegram_ids):
    for id in telegram_ids:
        bot.send_message(id, f'Опубликована новая новость в категории {news_details["category"]}\n{news_details["title"]}\n{news_details["description"]}\n\n\n<a href="127.0.0.1:8000{news_details["url"]}">Перейти к новости</a>', parse_mode='HTML')


def created_post(news_details):
    bot.send_message('@django_news_channel', f'''{news_details['title']}\n#{news_details['category']}\n{news_details['description']}\n\n\n<a href="127.0.0.1:8000{news_details['url']}">Перейти к новости</a>''', parse_mode='HTML')

# def send_news_details(news_details):
#     bot.send_photo('-4004087466', news_details['image'], f'''Опубликована новая новость\n{news_details['title']}\n{news_details['description']}\n{news_details['category']}''')


if __name__ == '__main__':
    bot.polling()

