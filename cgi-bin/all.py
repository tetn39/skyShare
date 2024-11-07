import cgi
import cgitb
import datetime
import io
import sqlite3
import sys

# debug mode
cgitb.enable()
# 文字化け対策
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 都道府県たち
prefs = ['北海道', '東北', '関東', '中部', '近畿', '中国', '四国', '九州']
pref_dict = {'北海道': 0, '東北': 1, '関東': 2, '中部': 3, '近畿': 4, '中国': 5, '四国': 6, '九州': 7}

# form 
form = cgi.FieldStorage()
recieve_date = form.getvalue('date')
recieve_pref = int(form.getvalue('pref'))

# datetime
now_datetime = datetime.datetime.now()

# 日付取得
now_date = now_datetime.strftime('%Y-%m-%d') # 現在の日付取得

# DB Date
all_check = False
date_check = ''
selected_date = ''
var_selected_date = False

if recieve_date == 'all':
    all_check = True

elif recieve_date == '0':
    date_check = now_date # 今日の日付のみ

elif recieve_date == '1':
    selected_date = now_datetime - datetime.timedelta(days=1)
    selected_date_strftime = selected_date.strftime('%Y-%m-%d')
    date_check = selected_date_strftime

else: # n日前まで
    var_selected_date = True
    selected_date = now_datetime - datetime.timedelta(days=int(recieve_date)) 
    selected_date_strftime = selected_date.strftime('%Y-%m-%d')

# sqlite
dbname = './DB/MAIN.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()
img_list = []
img = ''

cur.execute(f"SELECT * FROM SkyImages WHERE Pref = {pref_dict[prefs[recieve_pref]]}")
for row in cur:
    db_date = datetime.datetime.strptime(row[2], '%Y-%m-%d')
    if row[2] == date_check or all_check: # all, 0, 1
        img_list.append(f'<div><img src="../sky-images/{row[1]}" alt="えらー" class="all_show-imgs"><h3>{row[3]}</h3><p>{row[2]}</p></div>\n')
        
    elif var_selected_date:
            if selected_date <= db_date <= now_datetime:
               img_list.append(f'<div><img src="../sky-images/{row[1]}" alt="えらー" class="all_show-imgs"><h3>{row[3]}</h3><p>{row[2]}</p></div>\n')

img = ''.join(img_list)
if len(img_list) == 0:
    img += '<h3 style="margin: auto; margin-bottom: 20px ">画像はありません</h3>'
conn.close()

# selectedつける
def sele_check(value, date):
    if value == date:
        return ' selected'
    else:
        return ''

# html内容
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
    <script src="../js/inner.js"></script>
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
    <section class="main-content">
    <h1>{prefs[recieve_pref]}</h1>
            <div class="select_date">
                <form action="GET" action="/cgi-bin/all.py" enctype="multipart/form-data" id="form-date">
                        <select name="date" id="date" class="form-select">
                            <option value="0"{sele_check('0', recieve_date)}>今日</option>
                            <option value="1"{sele_check('1', recieve_date)}>昨日</option>
                            <option value="7"{sele_check('7', recieve_date)}>1週間前まで</option>
                            <option value="30"{sele_check('30', recieve_date)}>1か月前まで</option>
                            <option value="90"{sele_check('90', recieve_date)}>3か月前まで</option>
                            <option value="180"{sele_check('180', recieve_date)}>半年前まで</option>
                            <option value="360"{sele_check('360', recieve_date)}>1年前まで</option>
                            <option value="all"{sele_check('all', recieve_date)}>全て</option>
                        </select>
                        <input type="hidden" name="pref" value="{recieve_pref}">
                </form>
            </div>
    <div class="all_imgs" id="imgs">
            {img}
    </div>
</section>
    <footer>
        <p><small>Copyright SkyShare </small></p>
    </footer>
</body>
</html>
'''

# 送信
print('Content-type: text/html\n')
print(html)