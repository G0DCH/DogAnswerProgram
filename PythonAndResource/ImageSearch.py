import os, sys
import re
import pandas as pd
import six
import google.cloud.translate_v2 as translate
import matplotlib.image as img
import matplotlib.pyplot as pp
from tqdm import tqdm
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

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

KOREAN = 'ko'
ENGLISH = 'en'
# 영어 불용어 집합
englishStopWords = set(stopwords.words('english'))
WITHOUT = 'without'
KR_MANY = '들'
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

# TODO : 
# 1. 인덱스에 있는 값들이 번역 쿼리에 들었는지 검사
# 2. 없다면 단어 토큰화 -> lemma화 -> 영어에서 한글로 -> 한글에서 영어로
# 위 결과 단수 영어 단어 생성되고, 이것을 이용해서 번역 쿼리에 들었는지 검사.
def SearchImage(query):
    # 구글 번역기가 맞춤법 검사도 해줘서
    # 영어로 바꾸고 검사
    translatedQuery = TranslateQuery(query, KOREAN, ENGLISH).lower()

    # 검색어에 입력된 강아지 이름 찾기
    for name in dogNameList:
        if name not in translateNameMap.keys():
            translateNameMap[name] = TranslateQuery(name, KOREAN, ENGLISH).lower()

        translatedName = translateNameMap[name]

        if translatedName in translatedQuery:
            break

    if translatedName not in translatedQuery:
        print('{} is not in {}'.format(translatedName, translatedQuery))
        return None

    # 테이블 획득, 강아지 이름 제거
    targetTable = nameTableMap[name]
    translatedQuery = translatedQuery.replace(translateNameMap[name], '', 1).strip()

    # 쿼리 단어 토큰화 -> lemma화 -> 영어에서 한글로 번역 -> 한글에서 영어로 다시 번역.
    # 그 결과 불규칙 복수 명사 단수 명사 됨. ex) people -> person
    lemmaResult = MakeLemmas(translatedQuery)
    queryLemmas = lemmaResult[0]
    negativeLemmas = lemmaResult[1]

    # lemma를 기반으로 질의 확장
    extendResult = ExtendQuery(queryLemmas, negativeLemmas)
    extendLemmas = extendResult[0]
    extendNegativeLemmas = extendResult[1]

    resultImageNameList = []
    imageNameToRemoveList = []

    # negative만 쿼리에 적었는지 검사
    isDontHavePositive = extendLemmas == extendNegativeLemmas

    # 인덱스에 있는 값들이 번역 쿼리에 있는지 검사.
    # 있다면 값이 0 이상인 컬럼들 출력
    # 인덱스에 있는 값들이 번역 쿼리에 없다면
    # extendLemmas의 lemma를 테이블의 index들과 비교해서 있다면 컬럼을 출력
    for index in targetTable.index:
        lowIndex = index.lower()
        if isDontHavePositive or (lowIndex in translatedQuery) or (lowIndex in extendLemmas):
            detectedNames = GetNotZeroIndexes(targetTable, index)
            resultImageNameList.extend(detectedNames)
            if lowIndex in extendNegativeLemmas:
                imageNameToRemoveList.extend(detectedNames)

    resultImageNameList = list(set(resultImageNameList))

    for imageNameToRemove in imageNameToRemoveList:
        resultImageNameList.remove(imageNameToRemove)

    return resultImageNameList

def GetNotZeroIndexes(table, index):
    resultNameList = []
    series = table.loc[index] > 0
    # 검색 결과 이미지 이름 추가
    for resultName in series[series == True].index:
        resultNameList.append(resultName)

    return resultNameList

# lemma들을 받아서
# lemma들과 그 동의어들을 출력
def ExtendQuery(lemmas, negativeLemmas = None):
    extendQuery = []
    extendNegative = []
    for lemma in lemmas:
        synsets = wordnet.synsets(lemma)
        for synset in synsets:
            extendQuery.extend(synset.lemma_names())
            if lemma in negativeLemmas:
                extendNegative.extend(synset.lemma_names())

    result = list(set(extendQuery))
    negativeResult = list(set(extendNegative))

    return [result, negativeResult]

# 쿼리 단어 토큰화 -> lemma화 -> 영어에서 한글로 번역 -> 
# 복수 명사 단수로(사람들 -> 사람) -> 한글에서 영어로 다시 번역.
# 그 결과 불규칙 복수 명사 단수 명사 됨. ex) people -> person
def MakeLemmas(translatedQuery):
    wordTokens = word_tokenize(translatedQuery)
    # 불용어 제거
    wordTokens = RemoveStopWords(wordTokens)
    # 부정어 토큰
    negativeTokens = []
    if WITHOUT in wordTokens:
        # without 다음에 있는 단어 갖고오기
        for index in list(filter(lambda x: wordTokens[x] == WITHOUT, range(len(wordTokens)))):
            negativeTokens.append(wordTokens[index + 1])

        # without 제거
        wordTokens = [token for token in wordTokens if token != WITHOUT]
    lemmatizer = WordNetLemmatizer()
    queryLemmas = []
    # 부정어 리스트
    negativeLemmas = []

    for tokenWord in wordTokens:
        lemma = lemmatizer.lemmatize(tokenWord)
        lemma = TranslateQuery(lemma, ENGLISH, KOREAN)
        lemma = lemma.replace(KR_MANY, '')
        lemma = TranslateQuery(lemma, KOREAN, ENGLISH)
        
        if lemma not in queryLemmas:
            lowlemma = lemma.lower()
            queryLemmas.append(lowlemma)

            if tokenWord in negativeTokens:
                negativeLemmas.append(lowlemma)

    return [queryLemmas, negativeLemmas]

# 불용어 제거
def RemoveStopWords(wordTokens):
    result = []
    for wordToken in wordTokens:
        if wordToken not in englishStopWords:
            result.append(wordToken)
    
    return result

def TranslateQuery(query, source, target):
    text = query
    if isinstance(query, six.binary_type):
        text = query.decode('utf-8')
    
    result = client.translate(text, target_language=target, source_language=source)

    return result['translatedText']

def main():
    run()
    print(SearchImage('사람이 없는 시베리안 허스키'))

if __name__ == "__main__":
    main()
