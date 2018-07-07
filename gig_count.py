# -*- coding: utf-8 -*-
# Сбор данных об участниках тренировок на гичках

import sys
import json
import requests
import re
import time
import sqlite3


def request_comms(url, req_values):
    '''Запрашивает порцию комментариев и преобразует в текст'''
    res = requests.get(url, params=req_values)
    comms = json.loads(res.text)
    return comms

def parse_comms(comms, cur, con):
    '''Ищет комментарии со списком. Выделяет имена из списка,
    отделяет лишние данные, заносит в словарь.
    Если имя уже есть, увеличивает счетчик на 1'''

    sql_select = '''SELECT name, counter FROM members'''
    sql_insert = '''INSERT INTO 'members' (name, counter)
        VALUES (?, ?)
        '''
    if not comms['response']['items']: # Пустой ответ
        print('ENDED')
        return 1 # Стоп
    for comm in comms['response']['items']:
            if comm['from_id'] == -10916742: # От сообщества
                template1 = r'1\..*\n2\..*\n3\..*\n' # Список
                text = comm['text']
                has_list = re.search(template1, text)
                if has_list:
                    template2 = r'\d\.(.*\S.+)\n' # Элемент списка
                    in_list = re.findall(template2, text)
                    if in_list:
                        for member in in_list:
                            # Отделяем имя от мусора
                            words = member.split()
                            if len(words)>=2 and not ('(' in words[1] or ')' in words[1]):
                                    name = words[0]+' '+words[1]
                            else:
                                name = words[0]
                            values = (name, 1)

                            try:
                                cur.execute(sql_select)
                            except sqlite3.DatabaseError as err:
                                print('Error:', err)
                            for row in cur.fetchall():
                                stored_name, counter = row
                                in_base = 0
                                if name == stored_name:
                                    cur.execute('''INSERT INTO 'members' (counter)
                                    VALUES (?)''', counter + 1)
                                    con.commit()
                                    in_base = 1
                                if not in_base:
                                    try:
                                        cur.execute(sql_insert, values)
                                    except sqlite3.DatabaseError as err:
                                        print('Error:', err)
                                    else:
                                        con.commit()

##                            if name in members: # Дублирующиеся имена
##                                members[name] += 1
##                            else:
##                                members[name] = 1


def main():
    '''
    '''
    url = 'https://api.vk.com/method/board.getComments?'
    # Данные запроса из файла
    with open('req_values.txt', 'r', encoding='utf-8') as f:
        req_values = json.load(f)

    # Подключение к БД
    con = sqlite3.connect(r'gig_members.db')
    cur = con.cursor()

##    values = ('TEST', 1)
##    try:
##        cur.execute(sql_insert, values)
##    except sqlite3.DatabaseError as err:
##        print('Error:', err)
##    else:
##        con.commit()

    # Основной цикл
    for _ in range(100):
        comms = request_comms(url, req_values)
        stop = parse_comms(comms, cur, con)
        if stop:
            break
        req_values["start_comment_id"] += 100
        time.sleep(0.5)

    cur.close()
    con.close()

##    # Вывод
##    for mem, count in members.items():
##        print(mem, count)
##    print('TOTAL:', len(members))



if __name__=='__main__':
    main()