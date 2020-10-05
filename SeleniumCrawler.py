# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os, sys
import urllib.request
import argparse
import pandas as pd


path = os.path.dirname(os.path.abspath(__file__))
fileName = 'DogNames.csv'
dirName = 'DogImages'
driverName = 'chromedriver'

outputPath = os.path.join(path, dirName)

if not os.path.isdir(outputPath):
  os.makedirs(outputPath)

# 개 이름 불러오기
dogNames = pd.read_csv(os.path.join(path, fileName), encoding = 'utf-8')
# 웹 드라이버 실행
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')
browser = webdriver.Chrome(os.path.join(path, driverName), options=options)
header = {'Referer' : 'http://marketdata.krx.co.kr/mdi',
      'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
counter = 0
successCounter = 0

# 다운로드 할 이미지 개수
imageNumber = 10
#canContinue = False

for dogName in dogNames:
#  if '폼피츠' in dogName:
#    canContinue = True
#  if not canContinue:
#    continue

  url = "https://www.google.co.in/search?q="+dogName+"&source=lnms&tbm=isch"
  browser.get(url)
  imagePath = os.path.join(outputPath, dogName)
  imageURLs = []
  imageCount = 0

  if not os.path.exists(imagePath):
    os.makedirs(imagePath)

  for _ in range(imageNumber):
    browser.execute_script("window.scrollBy(0,10000)")

  for x in browser.find_elements_by_xpath('//img[contains(@class,"rg_i")]'):
    counter = counter + 1
    print ("Total Count:", counter)
    # 이미지를 클릭해서 큰 이미지를 불러옴
    try:
      x.click()
    except:
      continue
    for bigX in browser.find_elements_by_xpath('//img[not(contains(@class, "rg_i"))]'):
      imageURL = bigX.get_attribute('src')
      
      # 이상한거 긁어오면 다시
      if 'base64' in str(imageURL) or \
        imageURL is None or \
        imageURL in imageURLs:
        continue
      # png 타입이라고 생각하고 진행
      imageType = 'png'
      
      imageURLs.append(imageURL)

      # 403 에러가 뜨면 계속 진행
      try:
        req = urllib.request.Request(imageURL, headers=header)
        raw_img = urllib.request.urlopen(req).read()
      except urllib.request.HTTPError as e:
        print (e.read())
        continue
      
      File = open(os.path.join(imagePath , dogName + "_" + str(imageCount + 1) + "." + imageType), "wb")
      File.write(raw_img)
      File.close()
      successCounter = successCounter + 1
      imageCount = imageCount + 1
      print ("Succsessful Count:", successCounter)
      break

    if imageCount >= imageNumber:
      imageCount = 0
      break


print (successCounter, "pictures succesfully downloaded")

browser.close()