import re, datetime
from mlask import MLAsk

###############################################
# 設定

# 自分のユーザ名です。
# 変更を含む場合はその全てを指定します。
USERNAME = ['尾崎', '雄太', '尾崎雄太']

# 解析するトーク数です。
TALKNUM = 2

##############################################

# トークが行われた時間の表示とトーク内容とを正規表現で区別するため、パターンを登録します。
pattern_date = r'[0-9]{4}\.[0-9]{2}\.[0-9]{2}'
pattern_time = r'[0-9]{2}:[0-9]{2}'

# 処理が速くなるらしいのでコンパイルします。
re_date = re.compile(pattern_date)
re_time = re.compile(pattern_time)

# ファイルをパースして辞書型オブジェクトにします。
def parse(filename) :
    # トーク履歴を開いて行ごとに読み込みます。
    dat = open(filename, 'r')
    lines = dat.readlines()

    talkobj = []

    # 行ごとにループします。
    for (i, item) in enumerate(lines) :
        if item == '\n' :
            continue

        item_array = item.split()

        # トークの日付を表す行だった場合
        if re_date.match(item_array[0]) :
            if i > 1 :
                talkobj.append({'date': date, 'text': text})
            date_t = datetime.datetime.strptime(item_array[0], '%Y.%m.%d')
            date = datetime.date(date_t.year, date_t.month, date_t.day)
            text = []

        # 前のトークから溢れた行だった場合
        elif len(item_array) == 1 :
            if mytalk :
                text[len(text)-1] + item_array[0]

        # 普通に時間と名前とトーク内容だった場合
        else :
            if item_array[1] in USERNAME :
                mytalk = True
                text.append(item_array[2])

            else :
                mytalk = False
                continue
    
    return talkobj

if __name__ == '__main__':
    dat = parse('talk02.txt')

    anal = []
    for (i, day) in enumerate(dat) :
        orientation = {'POSITIVE': 0, 'mostly_POSITIVE': 0, 'NEUTRAL': 0, 'mostly_NEGATIVE': 0, 'NEGATIVE': 0}
        activation = {'ACTIVE': 0, 'mostly_ACTIVE': 0, 'NEUTRAL': 0, 'mostly_PASSIVE': 0, 'PASSIVE': 0}
        emotion = []
        representive = []
        for (j, talk) in enumerate(day['text']) :
            emotion_analyzer = MLAsk()
            o = emotion_analyzer.analyze(talk)

            if 'orientation' in o :
                orientation[o['orientation']] += 1
            
            if 'activation' in o :
                activation[o['activation']] += 1

            if 'emotion' in o :
                if o['emotion'] != None :
                    emotion.append(o['emotion'].values())

            if 'representative' in o :
                representive.append(o['representative'])

        anal.append({
            'date': day['date'],
            'orientation': orientation,
            'emotion': emotion,
            'activation': activation,
            'representive': representive
            })

    for (x, i) in enumerate(anal) :
        print('====================')
        print(i['date'])
        print('orientation:')
        print(i['orientation'])
        print('emotion:')
        print(i['emotion'])
        print('activation:')
        print(i['activation'])
        print('representive:')
        print(i['representive'])
        print('====================\n')
