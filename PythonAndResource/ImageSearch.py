import os, sys
import re
import pandas as pd
import google.cloud.translate_v2 as translate
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
        tableList.append([tableName, table])

    print(tableList[0])


def main():
    run()

if __name__ == "__main__":
    main()
