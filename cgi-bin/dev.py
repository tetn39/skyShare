import cgi
import io
import sqlite3
import sys


# 文字化け対策
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 都道府県たち
prefs = ['北海道', '東北', '関東', '中部', '近畿', '中国', '四国', '九州']
prefecturals = ['北海道']

# form 
form = cgi.FieldStorage()
sql = form.getvalue('db')



# sqlite
dbname = './DB/MAIN.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()
selected = ''

cur.execute(f"{sql}") # これをコメント外す
conn.commit()

# ここがうまくできてない ２つの条件を付けるとうまくいかない
# cur.execute(f'SELECT * FROM SkyImages WHERE Date <= "2023-02-27" and Pref = 3')
# cur.execute(f'SELECT * FROM SkyImages')

for row in cur:
    selected += f'{row}<br>'
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
    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="../css/for-py.css">
</head>
<body>
<header>
        <a href="/"><img src="../images/skyshaare2.png" alt="logo" class="logo"></a>
        <nav>
            <ul>
                <a href="/"><li>トップ</li></a>
                <a href="/upload.html"><li>アップロード</li></a>
            </ul>
        </nav>
    </header>
    <main class="db_selected">
    {selected}
    <br>
            <a href="/dev.html">back to dev.html</a>

    </main>
    <footer>
        <p><small>Copyright SkyShare </small></p>
    </footer>
</body>
</html>
'''


print('Content-type: text/html\n')

print(html)