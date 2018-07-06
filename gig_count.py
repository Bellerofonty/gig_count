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

def parse_comms(members, comms):
    '''Ищет комментарии со списком. Выделяет имена из списка,
    отделяет лишние данные, заносит в словарь.
    Если имя уже есть, увеличивает счетчик на 1'''
    if not comms['response']['items']: # Пустой ответ
        return members
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
                            if name in members: # Дублирующиеся имена
                                members[name] += 1
                            else:
                                members[name] = 1
    return members

def main():
    '''
    '''
    url = 'https://api.vk.com/method/board.getComments?'
    # Данные запроса из файла
    with open('req_values.txt', 'r', encoding='utf-8') as f:
        req_values = json.load(f)

    con = sqlite3.connect(r'gig_members.db')
    cur = con.cursor()
    sql = '''INSERT INTO 'members' (name, counter)
        VALUES (?, ?)
        '''
    values = ('TEST', 1)
    cur.execute(sql, values)

##    members = {}
##    for _ in range(100):
##        comms = request_comms(url, req_values)
##        members = parse_comms(members, comms)
##        req_values["start_comment_id"] += 100
##        time.sleep(0.5)

    cur.close()
    con.close()

##    # Вывод
##    for mem, count in members.items():
##        print(mem, count)
##    print('TOTAL:', len(members))



if __name__=='__main__':
    main()