import gspread
from flask import render_template
from oauth2client.service_account import ServiceAccountCredentials
from .models import app

def get_progress(app):
    with app.app_context():

        #Googleスプレッドシートへの認証情報
        scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('mystical-magnet-443807-q4-64e4c79c960c.json', scope)

        gc = gspread.authorize(credentials)

        # スプレッドシートを開く
        spreadsheet = gc.open_by_key('1taNBkibmIk3W427NqoJSXXMJW8DlTnOmS8sSqQSS7Bk')
        worksheet = spreadsheet.sheet1

        # データを取得
        data = worksheet.get_all_values()                                                 
        
        #データ数 11項目(0 - 10)
        PickupRowData = []
        TopTitle = ['NO','委託先','物件名称','延面積','建物用途','主担当','作図担当','業務状況','進捗%','全体工程','直近締日']
        for row in data:
            if (row[0] =='●'):
                PickupRowData.append([row[2], row[5], row[7], row[9],row[10], row[33], row[34], row[35],row[36], row[38], row[39]])
            else:
                continue
        
        PickupRowData.insert(0,TopTitle)

        return PickupRowData

@app.route('/')
def index():
    data = get_progress()
    return render_template('cute_paccho/ProjectProgressIndex.html', data=data)
