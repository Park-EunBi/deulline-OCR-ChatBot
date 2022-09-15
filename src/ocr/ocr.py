import pytesseract
from konlpy.tag import Twitter
from collections import Counter

from PIL import Image
import urllib.request
from io import BytesIO

import re
from konlpy.tag import Okt

import ssl
import random
import pymysql

ssl._create_default_https_context = ssl._create_unverified_context

# url으로 이미지 불러오기
url = "http://www.e-himart.co.kr/contents/content/upload/goods//00/16/90/51/68/ecd/KU75UA7050FXKR%20%EC%83%81%EC%84%B8%ED%8E%98%EC%9D%B4%EC%A7%80.jpg"
product_id = 5 # 크롤링으로 id 값 넘어온다
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
res = urllib.request.urlopen(req).read()
urlopen_img = Image.open(BytesIO(res))

text = pytesseract.image_to_string(urlopen_img, lang='kor')
file = open("./test.txt", "w")
for i in text:
    file.write(i)

file.close()

# 명사 빈도 분석
file = open('./test.txt', 'r')
text = file.read()
nlpy = Twitter()
nouns = nlpy.nouns(text)
count = Counter(nouns)

tag_count = []
tags = []
for n, c in count.most_common(100):
    dics = {'tag': n, 'count': c}
    if len(dics['tag']) >= 2 and len(tags) <= 49:
        tag_count.append(dics)
        tags.append(dics['tag'])

# 반복되는 명사를 담은 리스트
repeat_noun = []

for tag in tag_count:
    if int(tag['count']) >= 2:
        repeat_noun.append(tag['tag'])

# 필수 검색 단어 (사전 등록)
file_path = "./essential_noun.txt"

with open(file_path, encoding='utf-8') as f:
    essential_noun = f.read().splitlines()

noun = essential_noun + repeat_noun

# noun 이 들어있는 문장이 담긴 리스트
lines = []
result_remove_all = re.sub(r"\s", "", text)
result_remove_all = re.sub(r"\W,", "\n", result_remove_all)
result_remove_all = list(result_remove_all.split('.'))

# 최종적으로 추출한 문장을 담을 리스트
final_result = []
for text in result_remove_all:
    for n in noun:
        if (re.search(n, text)):
            final_result.append(text)

final_result = set(final_result)

okt = Okt()

# 띄어쓰기 함수
def spacing_okt(wrongSentence):
    tagged = okt.pos(wrongSentence)
    corrected = ""
    for i in tagged:
        if i[1] in ('Josa', 'PreEomi', 'Eomi', 'Suffix', 'Punctuation'):
            corrected += i[0]
        else:
            corrected += " " + i[0]
    if corrected[0] == " ":
        corrected = corrected[1:]
    return corrected

# 띄어쓰기 한 문장을 담을 리스트
spacing = []
for i in final_result:
    spacing.append(spacing_okt(i))

# 샘플 데이터 저장
num = random.randint(0, 15)
sample_data = spacing[num:num+2]

# db에 넣기 위해 한 문장으로 합치기
product_data = ' '.join(spacing)
sample_data = ' '.join(sample_data)

conn = pymysql.connect(host='localhost', user='root', password='-', db='deulline', charset='utf8')

cur = conn.cursor()
sql = "update product set product_data = %s where product_id = %s;"
cur.execute(sql, (product_data, product_id))
conn.commit()
conn.close()

conn = pymysql.connect(host='localhost', user='root', password='-', db='deulline', charset='utf8')

cur = conn.cursor()
sql = "insert into sample (sample_data, product_id) values(%s, %s)"
cur.execute(sql, (sample_data, product_id))
conn.commit()
conn.close()