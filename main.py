import telebot
from telebot import types, TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup

import random
from read_config import read_config
from other_postgres import add_new_user, check_user_in_db
from first_start import first_start
from select_word import select_word

buttons = []

state_storage = StateMemoryStorage()
token = read_config('settings.ini')
bot = telebot.TeleBot(token['Token']['telegram_token'])

@bot.message_handler(commands=['start'])
def bot_start(message):
    chat_id = str(message.chat.id)
    user_name = str(message.from_user.username)
    # bot.send_message(message.chat.id, f'Привет, {user_name}')
    if not check_user_in_db(chat_id):
        bot.send_message(message.chat.id, f'Привет, {user_name}')
        add_new_user(user_name=user_name, chat_id_telegram=chat_id)
    # else:
    #     bot.send_message(message.chat.id, f'{user_name} давай продолжим учиться!')
        
#______________________________________________________________________________________________________
        
    words = select_word(str(message.chat.id))
    markup = types.ReplyKeyboardMarkup(row_width=2)
    target_word = words[0]
    translate = words[1]
    target_word_btn = types.KeyboardButton(target_word)
    buttons.clear()
    buttons.append(target_word_btn)
    others = words[2]
    other_words_btns = [types.KeyboardButton(word) for word in others]
    buttons.extend(other_words_btns)
    random.shuffle(buttons)
    # next_btn = types.KeyboardButton(Command.NEXT)
    # add_word_btn = types.KeyboardButton(Command.ADD_WORD)
    # delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
    # buttons.extend([next_btn, add_word_btn, delete_word_btn])

    markup.add(*buttons)

    greeting = f"Выбери перевод слова:\n🇷🇺 {translate}"
    bot.send_message(message.chat.id, greeting, reply_markup=markup)
    bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data: # type: ignore
        data['target_word'] = target_word
        data['translate_word'] = translate
        data['other_words'] = others
        
        
        
        
        
        
    # create_cards(message)
        

    
    
        
        
        
        
        
        
class MyStates(StatesGroup):
    target_word = State()
    translate_word = State()
    another_words = State()
        
        
        
        
# @bot.message_handler()
# def create_cards(message):
#     words = select_word(str(message.chat.id))
#     markup = types.ReplyKeyboardMarkup(row_width=2)
#     target_word = words[0]
#     translate = words[1]
#     target_word_btn = types.KeyboardButton(target_word)
#     buttons.clear()
#     buttons.append(target_word_btn)
#     others = words[2]
#     other_words_btns = [types.KeyboardButton(word) for word in others]
#     buttons.extend(other_words_btns)
#     random.shuffle(buttons)
#     # next_btn = types.KeyboardButton(Command.NEXT)
#     # add_word_btn = types.KeyboardButton(Command.ADD_WORD)
#     # delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
#     # buttons.extend([next_btn, add_word_btn, delete_word_btn])

#     markup.add(*buttons)

#     greeting = f"Выбери перевод слова:\n🇷🇺 {translate}"
#     bot.send_message(message.chat.id, greeting, reply_markup=markup)
#     bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data: # type: ignore
#         data['target_word'] = target_word
#         data['translate_word'] = translate
#         data['other_words'] = others
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

if __name__ == '__main__':
    first_start()
    print('Bot is running')
    bot.polling()
    print('Bot is running')
    print('Bot is running')