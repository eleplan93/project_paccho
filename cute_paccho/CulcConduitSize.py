import gspread
from flask import render_template
from oauth2client.service_account import ServiceAccountCredentials
from .models import app

def get_spredsheet_data(app):
    with app.app_context():

        #Googleスプレッドシートへの認証情報
        scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('mystical-magnet-443807-q4-64e4c79c960c.json', scope)

        gc = gspread.authorize(credentials)

        # スプレッドシートを開く
        spreadsheet = gc.open_by_key('1CigEfuCvnvkeditOI3cIf1RhL5fkPZ-1nfq5JyzDoDE')
        AboutConduit = spreadsheet.worksheet('ConduitDataSheet')
        AboutCable = spreadsheet.worksheet('CableDataSheet')

        # データを取得
        conduit_data = AboutConduit.get_all_values()
        cable_data = AboutCable.get_all_values()

        return conduit_data, cable_data

@app.route('/')
def index_two():
    data = get_spredsheet_data()
    return render_template('cute_paccho/CulcConduitSize.html', data=data)


def judge_roop_narrow(x,y,section_area,conduit_data):
    decide = ""  #決定した配管サイズ

    for j in range(x,y,1):
        if section_area > int(conduit_data[j][4]):
            decide = conduit_data[j][2]
            return decide
        else:
            continue

    decide ='適合なし'
    return decide

def judge_roop_wide(x,y,section_area,conduit_data):
    decide = ""  #決定した配管サイズ

    for j in range(x,y,1):
        if section_area > int(conduit_data[j][4]):
            decide = conduit_data[j][2]
            return decide
        else:
            continue
    
    decide ='適合なし'
    return decide
    
# ▼ MAIN CODE
def CulculationConduitSize(CableName, CableNumber):
    
    conduit_data, cable_data = get_spredsheet_data(app)
    section_area = 0 #ケーブル断面積変数
    SmallSizeList = [['厚鋼電線管',''],['薄鋼電線管',''],['ねじなし電線管',''],['PF, CD管',''],['FEP管','']]
    BigSizeList = [['厚鋼電線管',''],['薄鋼電線管',''],['ねじなし電線管',''],['PF, CD管',''],['FEP管','']]
    
    for i in cable_data:
        if CableName == i[1]:
            section_area = int(i[3]) * CableNumber
            break
        else:
            continue
        
    x = 0 # list start NO
    y = 0 # list end NO

    # 厚鋼計算 32%
    x = 1
    y = 10
    SmallSizeList[0][1] = judge_roop_narrow(x,y,section_area,conduit_data)

    # 薄鋼計算 32%
    x = 11
    y = 17
    SmallSizeList[1][1] = judge_roop_narrow(x,y,section_area,conduit_data)

    # ねじなし計算 32%
    x = 18
    y = 24
    SmallSizeList[2][1] = judge_roop_narrow(x,y,section_area,conduit_data)

    # PF・CD計算 32%
    x = 25
    y = 29
    SmallSizeList[3][1] = judge_roop_narrow(x,y,section_area,conduit_data)

    # FEP計算 32%
    x = 30
    y = 38
    SmallSizeList[4][1] = judge_roop_wide(x,y,section_area,conduit_data)

    # 厚鋼計算 48%
    x = 1
    y = 10
    BigSizeList[0][1] = judge_roop_wide(x,y,section_area,conduit_data)

    # 薄鋼計算 48%
    x = 11
    y = 17
    BigSizeList[1][1] = judge_roop_wide(x,y,section_area,conduit_data)

    # ねじなし計算 48%
    x = 18
    y = 24
    BigSizeList[2][1] = judge_roop_wide(x,y,section_area,conduit_data)

    # PF・CD計算 48%
    x = 25
    y = 29
    BigSizeList[3][1] = judge_roop_wide(x,y,section_area,conduit_data)

    # FEP計算 48%
    x = 30
    y = 38
    BigSizeList[4][1] = judge_roop_wide(x,y,section_area,conduit_data)

    return SmallSizeList, BigSizeList
