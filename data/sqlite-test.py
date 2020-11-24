import sqlite3

# connect to database
db_name = "C:/Users/Ivan/Coding/sqlite/league.db"
conn = sqlite3.connect(db_name)

c = conn.cursor()

sql = "INSERT INTO Test VALUES (3, 'Peanut', null)"
c.execute(sql)

conn.commit()
conn.close()
