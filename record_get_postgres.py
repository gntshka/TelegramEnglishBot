from read_config import read_config
import psycopg2

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