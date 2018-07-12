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

def parse_comms(comms, offset):
    '''Ищет комментарии со списком. Выделяет имена из списка,
    отделяет лишние данные, заносит в словарь.
    Если имя уже есть, увеличивает счетчик на 1.
    Если комментарии закончились, возвращает 1 для остановки осн. цикла'''

    new_members = []
    # Если комментарии кончились (api дает один последний комментарий)
    if int(comms['response']['count']) <= offset:
        print('ENDED', comms['response']['count'], offset)
        return new_members, 1 # Стоп
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
                            new_members.append(name)

    return new_members, 0

def db_insert(con, cur, new_members):
    '''Записывает полученные имена в БД.
    Если имя уже есть, увеличивает счетчик на 1'''

    sql_insert = '''INSERT INTO 'members'(name, counter)
    VALUES (?,?)'''
    sql_update = '''UPDATE members SET counter=:counter WHERE name=:name'''

    for name in new_members:
        cur.execute('''SELECT name, counter FROM members WHERE name=:name''', {'name': name})
        row = cur.fetchone()
        if row: # Имя есть в БД
            stored_name, counter = row
            cur.execute(sql_update, {'counter':counter + 1, 'name': stored_name})
        else:
            cur.execute(sql_insert, (name, 1))
        con.commit()

def main():
    url = 'https://api.vk.com/method/board.getComments?'
    # Данные запроса из файла
    with open('req_values.txt', 'r', encoding='utf-8') as f:
        req_values = json.load(f)

    # Подключение к БД
    con = sqlite3.connect(r'gig_members.db')
    cur = con.cursor()

    # Очистка таблицы
    cur.execute('''DELETE FROM members''')
    con.commit()

    # Основной цикл
    for _ in range(10000):
        # Запрос порции комментариев (max=100)
        comms = request_comms(url, req_values)
        # Парсинг комментариев, выделение имен
        new_members, stop = parse_comms(comms, req_values["offset"])
        # Запись имён в БД с количеством посещений
        db_insert(con, cur, new_members)
        if stop: # Комментарии в теме кончились
            break
        req_values["offset"] += 100
        time.sleep(0.5)

    # Вывод
    cur.execute('''SELECT name, counter FROM members''')
    for row in cur.fetchall():
        name, counter = row
        print(name, counter)

    cur.close()
    con.close()

if __name__=='__main__':
    main()