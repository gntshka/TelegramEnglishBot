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
        
def drop_tables():
    users = '''
    DROP TABLE users;
    '''
    
    record_sql(users)
        
def create_table_users():
    drop_tables()
    users = '''
    CREATE TABLE users(
        user_id SERIAL PRIMARY KEY, 
        user_name VARCHAR(100), 
        user_id_telegram VARCHAR(100)
    );
    '''
    record_sql(users)

def add_new_user(user_name, user_id_telegram):
        new_user = ('''
        INSERT INTO users(user_name, user_id_telegram) VALUES(%s, %s);
        ''')
        user = user_name, user_id_telegram
        record_sql(new_user, user)
        
        
if __name__ == '__main__':
    create_table_users()