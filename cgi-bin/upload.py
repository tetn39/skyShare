import base64
import cgi
import datetime
import io
import sqlite3
import sys

# 文字化け対策
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# pref参考用
pref_dict = {'北海道': 0, '青森県': 1, '岩手県': 1, '宮城県': 1, '山形県': 1, '福島県': 1, '栃木県': 2, '群馬県': 2, '茨城県': 2, '埼玉県': 2, '千葉県': 2, '東京都': 2, '神奈川県': 2, '新潟県': 3, '長野県': 3, '山梨県': 3, '静岡県': 3, '富山県': 3, '岐阜県': 3, '石川県': 3, '福井県': 3, '愛知県': 3, '滋賀県': 4, '三重県':4, '奈良県': 4, '和歌山県': 4, '京都府': 4, '大阪府': 4, '兵庫県': 4, '鳥取県': 5, '岡山県': 5, '島根県': 5, '広島県': 5, '山口県': 5, '香川県': 6, '徳島県': 6, '高知県': 6, '愛媛県': 6, '福岡県': 7, '大分県': 7, '佐賀県': 7, '長崎県': 7, '熊本県': 7, '宮崎県': 7, '鹿児島県': 7, '沖縄県': 7} 


# form formの内容入れる
form = cgi.FieldStorage()

# formの内容取得
img = form.getvalue('img')
address = form.getvalue('address')
selected_date = form.getvalue('date')

# b64にencodeして、decodeする
b64 = base64.b64encode(img)
b64_decoded = base64.b64decode(b64)

# 保存するpath指定
now_datetime = datetime.datetime.now()

# 日付取得
# date = now_datetime.strftime('%Y-%m-%d') # 現在の日付取得(使わない)
img_date = now_datetime.strftime('%Y-%m-%d-%H-%M-%S')

# img名設定
img_name = f'{img_date}.jpg'
download_path = f'./sky-images/{img_name}'

# decodeしたものをpathに保存
with open(download_path, mode='wb') as f:
    f.write(b64_decoded)

# sqlite
dbname = './DB/MAIN.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()


# INSERT
cur.execute(f'INSERT INTO SkyImages (ImageName, Date, Address, Pref) VALUES ("{img_name}", "{selected_date}", "{address}", "{pref_dict[address]}")')
conn.commit()

cur.execute('SELECT * FROM SkyImages')

selected = ''
for row in cur:
    selected += f'{row}<br>\n'
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
    <link rel="stylesheet" href="../css/style.css">
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
    <main class="uploadp-main">
    <h1>アップロード完了</h1>
    <br>
    <h2>選択した都道府県</h2>
    <p class="upload-left">{address}</p>
    <h2>選択した画像</h2>
    <img src="../{download_path}" width="100px" alt="予期せぬエラーが発生しました" class="upload-left">
    <p hidden>{selected}</p>
    <a href="../upload.html"><h3>投稿ページに戻る</h3></a>
    </main>
</body>
</html>
'''

print('Content-type: text/html\n')
print(html)




# b64 encode
# https://kosuke-space.com/python_image_binary
# venv 使うこと