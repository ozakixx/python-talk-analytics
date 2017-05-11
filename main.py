from janome.tokenizer import Tokenizer

if __name__ == '__main__':
    talk = open('talk01.txt', 'r')
    lines = talk.readlines()

    for (i, item) in enumerate(lines):
        dat = item.split()
        print(dat)
