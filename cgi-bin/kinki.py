import io
import random
import sqlite3
import sys


# 文字化け対策
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# 地域
pref = 4

# sqlite
dbname = './DB/MAIN.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()
img_list = []
max_img = 2
img = ''


cur.execute(f"SELECT * FROM SkyImages WHERE Pref = {pref}")
for row in cur:
    img_list.append(f'<img src="../sky-images/{row[1]}" alt="えらー" class="show-imgs">')
img_4 = random.sample(img_list, min(max_img, len(img_list)))
img = ''.join(img_4)
conn.close()


html = f'''\
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>Sky Share</title>
    <link rel="shortcut icon" href="../images/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="../images/apple-touch-icon.png">
    <link rel="stylesheet" href="../css/sanitize.css">
    <link rel="stylesheet" href="../css/for-py.css">

</head>
<body>
    <a href="/cgi-bin/all.py?date=all&pref=4" target="_top">
    <div class="top-show">
    <div class="obj">
        <h2>近畿</h2>
        <div class="imgs">
            {img}
    </div>
    </div>
    </div>
    </a>
</body>
</html>
'''


print('Content-type: text/html\n')

print(html)