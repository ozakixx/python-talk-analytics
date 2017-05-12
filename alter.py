import re, datetime, csv
from mlask import MLAsk

###############################################
# 設定

# 自分のユーザ名です。
# 変更を含む場合はその全てを指定します。
USERNAME = '尾崎雄太'

# 解析するトーク数です。
TALKNUM = 21

##############################################

# トークが行われた時間の表示とトーク内容とを正規表現で区別するため、パターンを登録します。
pattern_date = r'[0-9]{4}\/[0-9]{2}\/[0-9]{2}'
pattern_time = r'[0-9]{2}:[0-9]{2}'

# 処理が速くなるらしいのでコンパイルします。
re_date = re.compile(pattern_date)
re_time = re.compile(pattern_time)

# データ格納用
result = []

# パース用関数
def parse(f) :
    # トーク履歴を開いて行ごとに読み込みます。
    _dat = open(f, 'r')
    _lines = _dat.readlines()
    _dat.close()
    
    _res = []
    for (i, _line) in enumerate(_lines) :
        if _line == '\n' :
            continue
        
        _line_arr = _line.split()

        if _line_arr == [] :
            continue
        
        if re_date.match(_line_arr[0]) :
            _date = _line_arr[0][0:10]

        if len(_line_arr) == 3 :
            if _line_arr[1] == USERNAME :
                _res.append((_date, _line_arr[2]))
    
    return _res

res = {}
# 解析用関数
def analyze(d) :
    _date = d[0]
    _txt = d[1]

    if _date in res :
        _tmp = res[_date]
        _ori = _tmp['orientation']
        _act = _tmp['activation']

    else :
        _ori = {'POSITIVE': 0, 'mostly_POSITIVE': 0, 'NEUTRAL': 0, 'mostly_NEGATIVE': 0, 'NEGATIVE': 0}
        _act = {'ACTIVE': 0, 'mostly_ACTIVE': 0, 'NEUTRAL': 0, 'mostly_PASSIVE': 0, 'PASSIVE': 0}

    emotion_analyzer = MLAsk()
    o = emotion_analyzer.analyze(_txt)

    if 'orientation' in o :
        _ori[o['orientation']] += 1
    
    if 'activation' in o :
        _act[o['activation']] += 1

    res[_date] = {'orientation': _ori, 'activation': _act}

def main() :
    for attempt in range(TALKNUM) :
        filename = 'talk' + '{0:02d}'.format(attempt+2) + '.txt' 
        print(filename)

        dat = parse(filename)

        for (i, item) in enumerate(dat) :
            analyze(item)
    output = ['date,PASSIVE,mostly_PASSIVE,NEUTRAL,mostly_ACTIVE,ACTIVE,NEGATIVE,mostly_NEGATIVE,NEUTRAL,mostly_POSITIVE,POSITIVE']        
    for d in res :
        date = d
        act_p = str(res[d]['activation']['PASSIVE'])
        act_mp = str(res[d]['activation']['mostly_PASSIVE'])
        act_n = str(res[d]['activation']['NEUTRAL'])
        act_ma = str(res[d]['activation']['mostly_ACTIVE'])
        act_a = str(res[d]['activation']['ACTIVE'])
        ori_n = str(res[d]['orientation']['NEGATIVE'])
        ori_mn = str(res[d]['orientation']['mostly_NEGATIVE'])
        ori_n = str(res[d]['orientation']['NEUTRAL'])
        ori_mp = str(res[d]['orientation']['mostly_POSITIVE'])
        ori_p = str(res[d]['orientation']['POSITIVE'])

        row = [date, act_p, act_mp, act_n, act_ma, act_a, ori_n, ori_mn, ori_n, ori_mp, ori_p]
        output.append(row)
        
    csvfile = open('data.csv', 'w')
    writer = csv.writer(csvfile, lineterminator='\n')
    writer.writerows(output)
    
    csvfile.close()
    print('complete')

if __name__ == '__main__' :
    main()
