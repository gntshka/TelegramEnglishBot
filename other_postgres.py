from record_get_postgres import record_sql, get_sql
        
def add_word(duet, user_id):
    new_word = '''
    INSERT INTO words(english_word, russian_word) VALUES(%s, %s);
                '''
    word = duet
    record_sql(new_word, word)
    word_id = get_word(duet[0])[0]
    record_users_words(word_id, user_id)
            
def get_word(word:str) -> tuple:
    finder = '''
    SELECT * FROM words
    WHERE english_word = %s;
    '''
    
    result = get_sql(finder, (word, ))
    return result # type: ignore

def count_words():
    counter = '''
    SELECT COUNT(*) FROM words;
    '''
    return get_sql(counter)
        
def record_users_words(word_id, user_id):
    record = '''
    INSERT INTO users_words(word_id, user_id, flag) VALUES(%s, %s, %s);
            '''
    values_ = word_id, user_id, 1
    record_sql(record, values_)

def add_new_user(user_name, chat_id_telegram):
        new_user = ('''
        INSERT INTO users(user_name, chat_id_telegram) VALUES(%s, %s);
        ''')
        user = user_name, chat_id_telegram
        record_sql(new_user, user)
        if int(chat_id_telegram) != 1:
            i = 1
            user_id = get_user(chat_id_telegram)[0] # type: ignore
            while i <= count_words()[0]: # type: ignore
                record_users_words(i, user_id)
                i += 1
            
def get_user(chat_id_telegram:str):
    finder = '''
    SELECT * FROM users
    WHERE chat_id_telegram = %s;
    '''
    
    user = get_sql(finder, (chat_id_telegram, ))
    return user

def check_user_in_db(chat_id_telegram:str):
    user = get_user(chat_id_telegram)
    return False if user == None else True
