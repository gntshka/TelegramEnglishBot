from other_postgres import add_word
from create_postgres import create_table_users

def first_start():    
    create_table_users()
    def read_file(name_file:str) -> list:
        all_lines = None
        with open(name_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            all_lines = lines
        return all_lines

    main_words_d = read_file('main_words.txt')

    main_words = []

    for i in main_words_d:
        i = i.strip().split(sep=' - ')
        main_words.append(tuple(i))

    for i in main_words:
        add_word(i, 1)
        
if __name__ == '__main__':
    first_start()