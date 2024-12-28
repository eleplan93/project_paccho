# 幹線計算ソフト
# 配線種類未対応、周波数未対応、許容電流未対応

import math

# ==Dictionary== k value & voltage
k_and_voltage1 = {'k_value':1,'voltage':100,'effeciency':0.95}
k_and_voltage2 = {'k_value':1.732,'voltage':200,'effeciency':0.8}
k_and_voltage = [k_and_voltage1,k_and_voltage2]

# ==Dictionary== voltage drop range
drop_range1 = {'length':0.06,'drop':3}
drop_range2 = {'length':0.12,'drop':5}
drop_range3 = {'length':0.2,'drop':6}
drop_range4 = {'length':1,'drop':7}
drop_range =[drop_range1,drop_range2,drop_range3,drop_range4]

# ==List== Resistance & Reactance & impedance of EM-CET cable
rri_ce50 = [
[2,12,0.0992,11.4,10.8,9.66],
[3.5,6.76,0.0914,6.45,6.12,5.46],
[5.5,4.34,0.0914,4.15,3.95,3.53],
[8,2.98,0.087,2.86,2.72,2.44],
[14,1.71,0.0828,1.65,1.58,1.42],
[22,1.08,0.082,1.05,1.01,0.913],
[38,0.626,0.0771,0.619,0.597,0.547],
[60,0.397,0.0768,0.401,0.391,0.364],
[100,0.239,0.0773,0.251,0.249],
[150,0.16,0.0744,0.175,0.176],
[200,0.121,0.0755,0.139,0.142,0.142],
[250,0.0985,0.0739,0.117,0.121,0.123],
[325,0.077,0.0723,0.096,0.101,0.105],
]

rri_cet50 = [
    [14,1.71,0.107,1.66,1.59,1.43],
    [22,1.08,0.103,1.06,1.02,0.926],
    [38,0.626,0.0955,0.624,0.605,0.558],
    [60,0.397,0.0913,0.406,0.397,0.372],
    [100,0.239,0.0881,0.255,0.254,0.244],
    [150,0.159,0.0846,0.177,0.18,0.178],
    [200,0.121,0.0859,0.142,0.146,0.148],
    [250,0.0981,0.0836,0.119,0.125,0.129],
    [325,0.0764,0.0816,0.099,0.104,0.11],
]

# (STEP 1) 電気方式の選択
def decide_elec_spec(ElecSpec):
    if ElecSpec == '単相3線式(200/100V)':
        elec_way = 0
    elif ElecSpec == '三相3線式(200V)':
        elec_way = 1
    else:
        elec_way = 0
    
    return elec_way


# (STEP 2) 電気容量計算
def decide_load(elec_way,ElecCapacity,voltage,k_v):
    current_value = ( ElecCapacity *1000 )

    if elec_way == 0:
        current_value = current_value / voltage / k_v['effeciency']
    else:
        current_value = current_value / voltage / 1.732 /k_v['effeciency']
    
    return current_value

# (STEP 3) 幹線長入力 km換算
def decide_length(FeederLength):

    cable_length = FeederLength / 1000

    return cable_length

# (STEP 6) 電圧降下率設定
def culc_impe(kind_of_cable,k_v,k_value,current_value,cable_length,voltage,jadge_value):
    for check_level in kind_of_cable:
        #インピーダンス計算　Rcos*Xsin = Rcos*sqrt(1-cos^2)
        phase1 = check_level
        sin = math.sqrt ( 1 - k_v['effeciency']**2 )

        impedance = phase1[1] * k_v['effeciency'] + phase1[2] * sin

        #電圧降下計算
        voltage_drop = k_value * current_value * cable_length * impedance
        voltage_drop_per = ( voltage_drop / voltage ) * 100
        
        if voltage_drop_per < jadge_value:
            return voltage_drop_per,phase1

# Main code
def CulcVoltageDrop(ElecSpec,ElecCapacity,FeederLength):

    elec_way = decide_elec_spec(ElecSpec)
    
    # (STEP 4) 電気方式によるK値の決定
    k_v = k_and_voltage[elec_way]

    k_value = k_v['k_value']
    voltage = k_v['voltage']

    current_value = decide_load(elec_way,ElecCapacity,voltage,k_v)
    cable_length = decide_length(FeederLength)
    
    # (STEP 5) 電圧降下率設定
    for drop_r in drop_range:
        if cable_length < drop_r['length']:
            jadge_value = drop_r['drop']
            break

    # (STEP 6) インピーダンス、電圧降下率計算
    voltage_drop_per = 0
    Elements = []
    Answers = [['ケーブル種類','サイズ','電圧降下率','設定電圧降下率']]

    Elements =  [['k値','電圧','電流値','ケーブル長'],[str(k_value),str(voltage),str('{0:.2f}A'.format(current_value)),str(cable_length)]]

    # in cace of CE cable
    kind_of_cable = rri_ce50

    voltage_drop_per,phase1 = culc_impe(kind_of_cable,k_v,k_value,current_value,cable_length,voltage,jadge_value)

    Answers += [['600V CE',str(phase1[0]),str('{0:.3f}%'.format(voltage_drop_per)),str('{0:.3f}%'.format(jadge_value))]]   

    # in cace of CET cable
    kind_of_cable = rri_cet50

    voltage_drop_per,phase1 = culc_impe(kind_of_cable,k_v,k_value,current_value,cable_length,voltage,jadge_value)
    
    Answers += [['600V CET',str(phase1[0]),str('{0:.3f}%'.format(voltage_drop_per)),str('{0:.3f}%'.format(jadge_value))]]
    
    return Elements, Answers



