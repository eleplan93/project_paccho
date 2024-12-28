# 接地線選択(C種,D種)

BreakerTrip = [20,30,40,50,60,75,100,125,150,175,200,225,250,300,350,400,500,600,800,1000]

CableSize = [2,5.5,8,14,22,38,60,100,150,200,250,325]

DecideCalculateTrip = None
DecideCableSize = None


def earth_cable_culc(CalculateTrip):
    # 開閉器容量入力  htmlにて入力
    
    # 接地線サイズ算出
    CalculateTrip=int(CalculateTrip)

    CalculateTrip *= 0.052

    # ケーブルサイズ選定
    for CableValue in CableSize:
        if CalculateTrip < CableValue:
            DecideCalculateTrip = CalculateTrip
            SubCableSize = CableValue
            break
        else:
            continue
            # DecideCalculateTrip = CalculateTrip
            # SubCableSize = CableSize[-1]  # CableSize の最後の要素を代入

    if SubCableSize <= 3.5:
        DecideCableSize = '2mm'
    else:
        DecideCableSize =str(SubCableSize)+'mm2'
    
    return DecideCalculateTrip, DecideCableSize


    