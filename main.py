import telebot
import configparser

def read_config(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config

token = read_config('settings.ini')
bot = telebot.TeleBot(token['Token']['telegram_token'])

@bot.message_handler(commands=['start'])
def bot_start(message):
    bot.send_message(message.chat.id, 'Правила просты, выбирай правильный перевод слова и жми "Далее"')
    russian_word = 'Someone'
    target_word = 'Someone'





if __name__ == '__main__':
    print('Hi')
    bot.polling()