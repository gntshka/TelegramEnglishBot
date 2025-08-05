import random
from other_postgres import get_all_user_words
from other_postgres import get_word_id

other_words = []

def select_word_id(chat_id_telegram):
    words_id = []
    for i in get_all_user_words(chat_id_telegram): # type: ignore
        words_id.append(i[2])
    random.shuffle(words_id)
    other_words.extend(words_id[1::])
    return words_id[0]

def select_word(chat_id_telegram):
    duet_word = get_word_id(select_word_id(chat_id_telegram)) 
    eng_word = duet_word[2]
    rus_word = duet_word[1]
    other_words_l = get_other_words(other_words) # type: ignore
    other_words.clear()
    return eng_word, rus_word, other_words_l

def get_other_words(other_words):
    i = 0
    words_list = []
    while i < 3:
        words_list.append(get_word_id(other_words[i])[2])
        i += 1
    return words_list




if __name__ == '__main__':
    print('')
    print(select_word('0'))
    print(other_words)
    print('')