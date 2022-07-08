from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from TikTokCollector import VideoStatisticsCollector
import pandas as pd
import json
import urllib

def write_document_to_file(document, file):
    json.dump(document, file)
    file.write("\n")
    file.flush()

videosMetadata = pd.read_json("../Data/VideoMetadata.json",lines=True)

options = Options()
#options.headless = True
options.add_argument("--window-size=1024,768")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
driver =  webdriver.Chrome("../chromedriver.exe",options=options)
api = VideoStatisticsCollector(driver)


invalid_characters = ['/','\\',':','*','?','<','>','|','\"']

sources = []
count = 0
for video in videosMetadata['Url']:
    if count % 1000 == 0:
        with open("../Data/Mp4/Mp4Info.json","a") as file:
            for line in sources:
                    write_document_to_file(line,file)
        sources=[]
    api.setUrl(video)
    try:
        newSource = {'Url':"",'Source':""}
        src=api.getContent()
        newSource['Source']=src
        newSource['Url']=video
        sources.append(newSource)
        count+=1
        print(newSource,count)
        filename = video
        for char in invalid_characters:
            filename = filename.replace(char,'')
        try:
            urllib.request.urlretrieve(src, 'D:/TikTokMp4/'+filename+'.mp4')
        except:
            print("Failed to download video: ",video)
    except:
        print("Failed to get source for ",video)
