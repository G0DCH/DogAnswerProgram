import os, sys
import re
import json
import pandas as pd
from tqdm import tqdm

path = os.path.dirname(os.path.abspath(__file__))
jsonDirName = 'DogDetected'
imageDirName = 'DogImages'

jsonBaseDirPath = os.path.join(path, jsonDirName)
imageBaseDirPath = os.path.join(path, imageDirName)

# 이미지와 json 파일 이름 변경
def ChangeName(basePath):
    # 개 이름 디렉토리 리스트
    dirList = os.listdir(basePath)
    replaceText = ''
    destText = ''
    for dirName in dirList:
        if dirName.find('개 ') >= 0:
            replaceText = '개 '
            destText = ''
        elif dirName.find('Aidi') >= 0:
            replaceText = 'Aidi'
            destText = '아이디'
        else:
            continue
                
        newDirName = dirName.replace(replaceText, destText, 1)
        # 개 이름 디렉토리 경로
        dogDirPath = os.path.join(basePath, dirName)
        newDogDirPath = os.path.join(basePath, newDirName)

        # 개 이름 디렉토리 속 json 파일 리스트
        jsonList = os.listdir(dogDirPath)

        # 숫자에 따라 파일 이름 정렬
        jsonList.sort(key=lambda x: int(re.sub('[\D]+', '', x)))

        # 파일 이름 변경
        for fileName in jsonList:
            newName = fileName.replace(replaceText, destText, 1)

            filePath = os.path.join(dogDirPath, fileName)
            newfilePath = os.path.join(dogDirPath, newName)

            os.rename(filePath, newfilePath)

        os.rename(dogDirPath, newDogDirPath)

def run():
    ChangeName(jsonBaseDirPath)
    ChangeName(imageBaseDirPath)


def main():
    run()

if __name__ == "__main__":
    main()
