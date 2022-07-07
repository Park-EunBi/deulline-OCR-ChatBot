import pytesseract
from konlpy.tag import Twitter
from collections import Counter

from PIL import Image
import urllib.request
from io import BytesIO

import re
from konlpy.tag import Okt

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# url으로 이미지 불러오기
url = "https://www.elandrs.com/upload/fckeditor/tempgoodsdesc/2022061655710849539.jpg"
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

print(spacing)