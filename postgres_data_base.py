from read_config import read_config
import psycopg2
#Добавить функцию дропа всех таблиц

config = read_config('settings.ini')
database = config['DB']['database']
user = config['DB']['user']
password = config['DB']['password']

def record_sql (action:str, params=None):
    conn = psycopg2.connect(database=database, user=user, password=password)
    if params == None:
        with conn.cursor() as cur:
            cur.execute(action)
            conn.commit()
        conn.close()
    else:
        with conn.cursor() as cur:
            cur.execute(action, params)
            conn.commit()
        conn.close()
        
def get_sql (action:str, params=None, mode=0):
    '''
    mode =  0-fetchone      Реализовано
            1-fetchmany     Не реализовано
            2-fetchall      Не реализовано
    '''
    
    conn = psycopg2.connect(database=database, user=user, password=password)
    if params == None:
        with conn.cursor() as cur:
            cur.execute(action)
            result = cur.fetchone()
        conn.close()
    else:
        with conn.cursor() as cur:
            cur.execute(action, params)
            result = cur.fetchone()
        conn.close()
    return result
        
        
def drop_tables():
    users_words = '''
    DROP TABLE users_words;
    '''
    record_sql(users_words)
    
    users = '''
    DROP TABLE users;
    '''
    record_sql(users)
    
    words = '''
    DROP TABLE words;
    '''
    record_sql(words)
    
def create_table_words():
    words = '''
    CREATE TABLE IF NOT EXISTS words(
        word_id SERIAL PRIMARY KEY, 
        russian_word VARCHAR(100), 
        english_word VARCHAR(100)
    );
    '''
    record_sql(words)

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
    
    
def create_table_users_words():
    table = '''
    CREATE TABLE IF NOT EXISTS users_words(
        record_id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(user_id),
        word_id INTEGER NOT NULL REFERENCES words(word_id),
        flag INTEGER NOT NULL CHECK(flag in(0, 1))
    );
    '''
    record_sql(table)
    
def record_users_words(word_id, user_id):
    record = '''
    INSERT INTO users_words(word_id, user_id, flag) VALUES(%s, %s, %s);
            '''
    values_ = word_id, user_id, 1
    record_sql(record, values_)
        
def create_table_users():
    drop_tables()
    users = '''
    CREATE TABLE IF NOT EXISTS users(
        user_id SERIAL PRIMARY KEY, 
        user_name VARCHAR(100), 
        chat_id_telegram VARCHAR(100)
    );
    '''
    record_sql(users)
    
    create_table_words()
    create_table_users_words()
    add_new_user('someone', '0')

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

if __name__ == '__main__':
    pass