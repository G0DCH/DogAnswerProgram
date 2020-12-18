import os, sys
import re
import json
import pandas as pd
from tqdm import tqdm

path = os.path.dirname(os.path.abspath(__file__))
jsonDirName = 'DogDetected'

jsonBaseDirPath = os.path.join(path, jsonDirName)
table = None

def read_json(jsonData, photoName):
    global table

    nameList = []
    confidenceList = []
    for data in jsonData:
        nameList.append(data['Name'])
        confidenceList.append(data['Confidence'])

    # 테이블이 없다면 생성, 아니라면 새로 추가된 데이터 병합
    tmpTable = pd.DataFrame(columns=[photoName], data=confidenceList, index=nameList)
    if table is None:
        table = tmpTable
    else:        
        table = pd.concat([table, tmpTable], axis=1)

    table = table.fillna(0)
    print(table)

def run():
    # 개 이름 디렉토리 리스트
    dirList = os.listdir(jsonBaseDirPath)
    for dirName in dirList:
        # 개 이름 디렉토리 경로
        jsonDogDirPath = os.path.join(jsonBaseDirPath, dirName)
        # 개 이름 디렉토리 속 json 파일 리스트
        jsonList = os.listdir(jsonDogDirPath)

        # 숫자에 따라 파일 이름 정렬
        jsonList.sort(key=lambda x: int(re.sub('[\D]+', '', x)))

        for jsonName in jsonList:
            jsonPath = os.path.join(jsonDogDirPath, jsonName)
            with open(jsonPath, 'r') as readFile:
                photoName = jsonName.split('.')[0]
                jsonData = json.load(readFile)
                read_json(jsonData, photoName)
                readFile.close()
        break


def main():
    run()

if __name__ == "__main__":
    main()
