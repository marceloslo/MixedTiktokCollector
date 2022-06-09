import pandas as pd
from selenium import webdriver
import TikTokCollector
import time
import json
import os
from datetime import datetime


def write_document_to_file(document, file):
    json.dump(document, file)
    file.write("\n")
    file.flush()

newVideos = pd.read_json("Data/VideosTemp.json",lines=True)

try:
    videos = pd.read_json("Data/VideoMetadata.json",lines=True)
except:
    videos = pd.DataFrame(columns=["Url",'User',"UserId","ProfileBio","Followers","Following","LikeCount","CollectionDate","Status"])

opts = webdriver.ChromeOptions()
opts.add_argument("--window-size=1024,768")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--no-sandbox")
driver =  webdriver.Chrome("./chromedriver.exe",options=opts)
api = TikTokCollector.VideoStatisticsCollector(driver)
newData=[]
today = datetime.now().strftime("%Y-%m-%d")
for url in newVideos['Url']:
    if url not in videos['Url'].to_list():
        print('Collecting '+url)
        api.setUrl(url)
        data=api.getMetadata()
        newData.append(data)
driver.quit()
print("Saving")
with open("Data/VideoMetadata.json","a") as file:
    for line in newData:
        write_document_to_file(line,file)

os.remove("Data/VideosTemp.json")