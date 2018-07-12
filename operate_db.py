import sqlite3

con = sqlite3.connect(r'gig_members.db')
##con.row_factory = sqlite3.Row
cur = con.cursor()

##cur.execute('''CREATE TABLE `members` (
##  `id` INT,
##  `name` VARCHAR(45) NOT NULL,
##  `surname` VARCHAR(45) NULL,
##  `counter` INT NOT NULL,
##  `last_seen` DATETIME NULL,
##  PRIMARY KEY (`name`));''')

names = ['00. Выход', 'Раева Полина', 'Раев Константан', 'Шаповалова Валя', 'Александр Конев', 'Маша Никитина', 'Пучков Сережа', 'Юра Кручиненко', 'Катя Клещёва', 'Ольга Сафонова', 'Головкин Иван', 'Кадонцева Ольга', 'Вадим Александров', 'Выход по', 'Александра Григорьева', 'Ольга Преображенская', 'Вадим Александров', 'Елена Ананьина', 'Алексей Лозинский', 'Святослав Преображенский', 'Александра Мороко', 'Михаил', 'Марианна', 'Элли Пономарева', 'Аглая Шенгер', 'Николай Фомин', 'Виталий Костыря', 'Дмитрий Мезерин', 'Алёна Фоминова', 'Лена Мухина', 'Марина Степанова', 'Александр Гагарин', 'Марина Карелина', 'Эльмира Хайрушева']
pre_names = ['00. Выход', 'Раева Полина', 'Раев Константан', 'Шаповалова Валя', 'Александр Конев']
pre_names2 = ['Раева Полина', 'Раев Константан', 'Александр Конев', 'not in list']

# Очистка таблицы
##cur.execute('''DELETE FROM members''')
##con.commit()

# Предзаполнение (тестовое)
##for name in pre_names:
##    cur.execute('''INSERT INTO members (name, counter) VALUES (?,?)''', (name, 1))
##con.commit()

# Занесение и обновление записей
##sql_insert = '''INSERT INTO 'members'(name, counter)
##    VALUES (?,?)
##    '''
##sql_update = '''UPDATE members SET counter=:counter WHERE name=:name'''
##for name in names:
##    cur.execute('''SELECT name, counter FROM members WHERE name=:name''', {'name': name})
##    row = cur.fetchone()
##    if row:
##        stored_name, counter = row
##        cur.execute(sql_update, {'counter':counter + 1, 'name': stored_name})
##        con.commit()
##    else:
##        cur.execute(sql_insert, (name, 1))
##        con.commit()

# Вывод
for row in cur.execute('''SELECT name, counter FROM members ORDER BY counter'''):
    print(row)

cur.close()
con.close()