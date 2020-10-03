# -*- coding: utf-8 -*-
import os, sys
from google_images_download import google_images_download

response = google_images_download.googleimagesdownload()

path = os.path.dirname(os.path.abspath(__file__))
fileName = 'DogNames.csv'
dirName = 'DogImages'

outputPath = os.path.join(path, dirName)

if not os.path.isdir(outputPath):
  os.makedirs(outputPath)

dogNames = open(os.path.join(path, fileName), 'r', encoding='utf-8').readline()

arguments = {"keywords" : dogNames, "limit" : 1, "print_urls" : False, "output_directory" : outputPath}
paths = response.download(arguments)