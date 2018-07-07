import sqlite3

con = sqlite3.connect(r'gig_members.db')
cur = con.cursor()

##cur.execute('''CREATE TABLE `members` (
##  `id` INT,
##  `name` VARCHAR(45) NOT NULL,
##  `surname` VARCHAR(45) NULL,
##  `counter` INT NOT NULL,
##  `last_seen` DATETIME NULL,
##  PRIMARY KEY (`name`));''')

cur.execute('''SELECT * FROM members''')
for row in cur.fetchall():
    name, counter = row
    print(name, counter)

cur.close()
con.close()