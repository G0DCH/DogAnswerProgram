import boto3
import os, sys
import re
import json
from tqdm import tqdm

path = os.path.dirname(os.path.abspath(__file__))
dirName = 'DogImages'
jsonDirName = 'DogDetected'

dirPath = os.path.join(path, dirName)
dirList = os.listdir(dirPath)
dirList.sort()
jsonBaseDirPath = os.path.join(path, jsonDirName)
jsonDirPath = ''


def detect_labels_local_file(photo):
    client=boto3.client('rekognition')

    with open(photo, 'rb') as image:
        try:
            response = client.detect_labels(Image={'Bytes': image.read()})
        except Exception as e:
            print(e)
            return 0

    # print('Detected labels in ' + photo)
    # for label in response['Labels']:
    #     print (label['Name'] + ' : ' + str(label['Confidence']))

    # 검출한 항목 json으로 저장
    jsonFilePath = os.path.join(jsonDirPath, os.path.basename(photo) + '.json')
    with open(jsonFilePath, 'w') as outfile:
        json.dump(response['Labels'], outfile, indent=4)
        outfile.close()

    return len(response['Labels'])

def run():
    global jsonDirPath

    if not os.path.isdir(jsonBaseDirPath):
        os.makedirs(jsonBaseDirPath)

    # isStopPoint = True

    for dirName in tqdm(dirList):
        # if dirName.find('벨기에 말리노이즈') >= 0:
        #     isStopPoint = False

        # if isStopPoint:
        #     continue
        
        myPath = os.path.join(dirPath, dirName)
        myPhotoList = os.listdir(myPath)    
        jsonDirPath = os.path.join(jsonBaseDirPath, dirName)

        # 해당 강아지의 디렉토리가 없다면 생성
        if not os.path.isdir(jsonDirPath):
            os.makedirs(jsonDirPath)

        # 숫자에 따라 파일 이름 정렬
        myPhotoList.sort(key=lambda x: int(re.sub('[\D]+', '', x)))

        # 해당 강아지 사진들에 대해서 검출
        for i in range(0, len(myPhotoList)):
            myPhotoPath = os.path.join(myPath, myPhotoList[i])

            photo = myPhotoPath

            label_count = detect_labels_local_file(photo)
            # print("Labels detected: " + str(label_count))

def main():
    run()


if __name__ == "__main__":
    main()
