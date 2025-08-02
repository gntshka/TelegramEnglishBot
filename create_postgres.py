from record_get_postgres import record_sql, get_sql
from other_postgres import add_new_user
       
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

if __name__ == '__main__':
    pass