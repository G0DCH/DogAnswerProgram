import os, sys
import re
import pandas as pd
import six
import google.cloud.translate_v2 as translate
import matplotlib.image as img
import matplotlib.pyplot as pp
from tqdm import tqdm

path = os.path.dirname(os.path.abspath(__file__))

tableDirName = 'VectorTables'
tableDirPath = os.path.join(path, tableDirName)

imageDirName = 'DogImages'
imageDirName = os.path.join(path, imageDirName)

# 개 이름과 테이블이 매핑된 것
nameTableMap = {}
dogNameList = []

# 한글 이름과 영어 이름이 매핑된 것
translateNameMap = {}

SOURCE_LANGUAGE = 'ko'
DEST_LANGUAGE = 'en'
client = translate.Client()

def run():
    LoadTable()

def LoadTable():
    global nameTableMap

    # 개 이름 테이블 리스트
    dirList = os.listdir(tableDirPath)
    for tableName in tqdm(dirList):
        # csv 파일 불러오기
        table = pd.read_csv(os.path.join(tableDirPath, tableName), index_col=0)
        dogName = str.split(tableName, '.')[0]
        nameTableMap[dogName] = table
        dogNameList.append(dogName)

def LoadImage(imagePath):
    return img.imread(imagePath)

def LoadImages(dirName, nameList):
    imageDirPath = os.path.join(imageDirName, dirName)

    images = []

    for name in nameList:
        imagePath = os.path.join(imageDirPath, name)
        images.append(LoadImage(imagePath))

    return images

def SearchImage(query):
    # 구글 번역기가 맞춤법 검사도 해줘서
    # 영어로 바꾸고 검사
    translatedQuery = TranslateQuery(query).lower()

    for name in dogNameList:
        if name not in translateNameMap.keys():
            translateNameMap[name] = TranslateQuery(name).lower()

        translatedName = translateNameMap[name]

        if translatedName in translatedQuery:
            break

    if translatedName not in translatedQuery:
        print('{} is not in {}'.format(translatedName, translatedQuery))
        return None

    # 테이블 획득
    targetTable = nameTableMap[name]

    print(targetTable.index)

def TranslateQuery(query):
    text = query
    if isinstance(query, six.binary_type):
        text = query.decode('utf-8')
    
    result = client.translate(text, target_language=DEST_LANGUAGE, source_language=SOURCE_LANGUAGE)

    return result['translatedText']

def main():
    run()

if __name__ == "__main__":
    main()
