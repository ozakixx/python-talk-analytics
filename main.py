import re
from mlask import MLAsk

# トークが行われた時間の表示とトーク内容とを正規表現で区別するため、パターンを登録します
pattern_date = r'[0-9]{4}\.[0-9]{2}\.[0-9]{2}'
pattern_time = r'[0-9]{2}:[0-9]{2}'

# 処理が速くなるらしいのでコンパイルします。
re_date = re.compile(pattern_date)
re_time = re.compile(pattern_time)

if __name__ == '__main__':
    # トーク履歴を開いて行ごとに読み込みます
    talk = open('talk02.txt', 'r')
    lines = talk.readlines()

    # 各行に対して処理をするループです
    for (i, item) in enumerate(lines):

        # 空行をキャンセルします
        if item == '\n':
            continue

        dat = item.split()
        if (re_date.match(dat[0])):
            print (dat)
