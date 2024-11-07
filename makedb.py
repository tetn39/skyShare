import sqlite3

dbname = './DB/MAIN.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()


cur.execute('CREATE TABLE SkyImages(ID INTEGER PRIMARY KEY AUTOINCREMENT, ImageName STRING UNIQUE, Date DATETIME, Address STRING, Pref INTEGER)')

# cur.execute('INSERT INTO SkyImages (ImageName, Date, Address) VALUES ("image1.jpg", "2023-06-20", "神奈川県")')

# conn.commit()

# cur.execute('SELECT * FROM SkyImages')

# for row in cur:
#     print(row)


conn.close()