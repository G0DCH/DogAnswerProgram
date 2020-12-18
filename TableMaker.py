import boto3
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

    if table is None:
        table = pd.DataFrame(columns=[photoName] ,data=confidenceList, index=nameList)

    print(table)

def run():
    # 개 이름 디렉토리 리스트
    dirList = os.listdir(jsonBaseDirPath)
    for dirName in dirList:
        # 개 이름 디렉토리 경로
        jsonDogDirPath = os.path.join(jsonBaseDirPath, dirName)
        # 개 이름 디렉토리 속 json 파일 리스트
        jsonList = os.listdir(jsonDogDirPath)
        for jsonName in jsonList:
            jsonPath = os.path.join(jsonDogDirPath, jsonName)
            with open(jsonPath, 'r') as readFile:
                photoName = jsonName.split('.')[0]
                jsonData = json.load(readFile)
                read_json(jsonData, photoName)
                readFile.close()
            break
        break


def main():
    run()

if __name__ == "__main__":
    main()
