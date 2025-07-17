import telebot
from read_config import read_config
from postgres_data_base import add_new_user
import postgres_data_base


token = read_config('settings.ini')
bot = telebot.TeleBot(token['Token']['telegram_token'])

@bot.message_handler(commands=['start'])
def bot_start(message):
    user_id = str(message.from_user.id)
    user_name = str(message.from_user.username)
    bot.send_message(message.chat.id, f'Привет, {user_name}')
    add_new_user(user_name=user_name, user_id_telegram=user_id)

if __name__ == '__main__':
    print('Bot is running')
    bot.polling()
