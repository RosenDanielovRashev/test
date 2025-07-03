import chardet

with open('fi.csv', 'rb') as f:
    result = chardet.detect(f.read())
    print(result)
