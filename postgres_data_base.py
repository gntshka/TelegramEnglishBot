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
    
def insert_main_words():
    pass
    
        
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

def add_new_user(user_name, chat_id_telegram):
        new_user = ('''
        INSERT INTO users(user_name, chat_id_telegram) VALUES(%s, %s);
        ''')
        user = user_name, chat_id_telegram
        record_sql(new_user, user)
        
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
    create_table_users()