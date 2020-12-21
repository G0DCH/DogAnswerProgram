import os, sys
import re
import pandas as pd
import google.cloud.translate_v2 as translate
import matplotlib.image as img
import matplotlib.pyplot as pp
from tqdm import tqdm

path = os.path.dirname(os.path.abspath(__file__))

tableDirName = 'VectorTables'
tableDirPath = os.path.join(path, tableDirName)

tableList = []

client = translate.Client()

def run():
    global tableList

    # 개 이름 테이블 리스트
    dirList = os.listdir(tableDirPath)
    for tableName in tqdm(dirList):
        # csv 파일 불러오기
        table = pd.read_csv(os.path.join(tableDirPath, tableName), index_col=0)
        tableList.append([str.split(tableName, '.')[0], table])

def LoadImage(imagePath):
    return img.imread(imagePath)

def LoadImages(dirName):
    imageDirPath = os.path.join(path, dirName)

def main():
    run()

if __name__ == "__main__":
    main()
