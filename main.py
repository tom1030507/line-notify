#導入需要的函式庫
import requests
import json
import datetime
from flask import Flask

#建立flask
app = Flask(__name__)

# 接收訊息
@app.route("/")
def callback():
    # 網站內容
    context = '''
    <h3>陳聖勳的專案</h3>
    <span>這是我做的一個<a href='https://github.com/tom1030507'>小專案</a></span>
    ''' 
    # 權杖
    token = '6Ldnx2c0F33pyD7DfLATEilNmB1g8jK1pwdbZIG52d1'
    time = datetime.datetime.now()
    if (time.hour==12 or time.hour==18):
        message = crawler()
        lineNotifyMessage(token, message)
    return context

# 發送訊息
def lineNotifyMessage(token, msg):
    # 參數設定
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg }
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code

def crawler():
    try:
        # 學校布告欄資料網址
        url = "https://www2.cshs.tc.edu.tw/ischool/widget/site_news/news_query_json.php"
        # 索取網站參數設定，沒有這個爬不到資料
        payload = {
            'field':'time',
            'order':'DESC',
            'pageNum':0,
            'maxRows':50,
            'keyword':'',
            'uid':'WID_91_2_dbe5afbc5332fba18d2d97938fd46077bb8bf64e',
            'tf':1,
            'auth_type':'user',
            'use_cache':1,
            }
        #爬蟲
        r = requests.post(url, data=payload)
        #"時間"格式轉換
        time = str(datetime.date.today())
        time = time.split('-')
        time = "/".join(time)
        #空陣列設置
        hot = []
        today = []
        #檢查回傳值是否正確
        if r.status_code == requests.codes.ok:
            r = r.text
        else:
            print("Error")
        #解碼成python的字典並轉成uft-8形式
        r = r.encode('utf-8').decode('utf-8') 
        r = json.loads(r)
        #用字典的方式判斷
        for i in range(1,50):
            #判斷如果是置頂公告或當日的新公告就加入不同的陣列
            if (r[i]['top']==1):
                hot.append(r[i]['title'])
            if (r[i]['time']==time):
                today.append(r[i]['title'])
        #重組訊息
        message = " \n置頂公告\n\n" + "\n".join(hot) + "\n\n" + time + "\n\n" + "\n".join(today) + "\n\n" + str(datetime.datetime.now())
    except:
        message = "Error"
    return message

#開始運作flask
if __name__ == "__main__":
    app.run(host='0.0.0.0')