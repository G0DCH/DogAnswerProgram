# -*- coding: utf-8 -*-
import os, sys
from bs4 import BeautifulSoup

# 수프 객체 return
def MakeSoup(path):
  data = open(path, "r", encoding = "utf-8")
  soup = BeautifulSoup(data, 'html.parser')

  return soup

def SoupToList(soup):
  # 수프 파일에서 개 이름만 추출
  paragraphs = soup.find_all('div', {'class' : 'wiki-paragraph'})
  skipCount = 0
  DogNameList = []
  for paragraph in paragraphs:
    contents = paragraph.contents
    if len(contents) > 0:
      if skipCount < 9:
        skipCount += 1
        continue
      content = contents[0]
      if '<' not in str(content):
        DogNameList.append(content)
        if '휘핏' in str(content):
          break
      else:
        DogNameList.append(content.text.strip())

  return DogNameList

path = os.path.dirname(os.path.abspath(__file__))
fileName = 'Dog.html'

# 수프 파일로 변경
soup = MakeSoup(os.path.join(path, fileName))
DogNameList = SoupToList(soup)

# csv 파일로 저장
import csv

outputName = 'DogNames.csv'

with open(os.path.join(path, outputName), 'w', newline = '', encoding = "utf-8") as outputFile:
  writer = csv.writer(outputFile)
  writer.writerow(DogNameList)