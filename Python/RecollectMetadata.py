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
videosMetadata = videosMetadata.to_dict('records')
options = Options()
#options.headless = True
options.add_argument("--window-size=1024,768")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
driver =  webdriver.Chrome("../chromedriver.exe",options=options)
api = VideoStatisticsCollector(driver)


invalid_characters = ['/','\\',':','*','?','<','>','|','\"']

sources = []
for line in videosMetadata:
    video = line['Url']
    api.setUrl(video)
    try:
        src=api.getContent()
        line['Content']=src
    except:
        print("Failed to get source for ",video)

with open('../Data/auxmetadata.txt','w') as file:
    for line in videosMetadata:
        write_document_to_file(line,file)