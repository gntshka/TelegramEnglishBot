import telebot
from read_config import read_config
from postgres_data_base import add_new_user
from postgres_data_base import check_user_in_db
from first_start import first_start
import postgres_data_base


token = read_config('settings.ini')
bot = telebot.TeleBot(token['Token']['telegram_token'])

@bot.message_handler(commands=['start'])
def bot_start(message):
    chat_id = str(message.chat.id)
    user_name = str(message.from_user.username)
    bot.send_message(message.chat.id, f'Привет, {user_name}')
    if not check_user_in_db(chat_id):
        add_new_user(user_name=user_name, chat_id_telegram=chat_id)
    else:
        bot.send_message(message.chat.id, f'{user_name} давай продолжим учиться!')

if __name__ == '__main__':
    first_start()
    print('Bot is running')
    bot.polling()