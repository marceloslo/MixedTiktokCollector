import pandas as pd
from selenium import webdriver
import TikTokCollector
import json
import os
from datetime import datetime


def write_document_to_file(document, file):
    json.dump(document, file)
    file.write("\n")
    file.flush()

newVideos = pd.read_json("./Data/VideosTemp.json",lines=True)

try:
    videos = pd.read_json("./Data/VideoMetadata.json",lines=True)
except:
    videos = pd.DataFrame(columns=["Url",'User',"UserId","ProfileBio","Followers","Following","LikeCount","CollectionDate","Status"])

driver =  webdriver.Chrome("./chromedriver.exe")
api = TikTokCollector.VideoStatisticsCollector(driver)
newData=[]
today = datetime.now().strftime("%Y-%m-%d")
for url in newVideos['Url']:
    print('Collecting '+url)
    api.setUrl(url)
    data=api.getMetadata()
    newData.append(data)
driver.quit()
print("Saving")
with open("./Data/VideoMetadata.json","a") as file:
    for line in newData:
        write_document_to_file(line,file)

#os.remove("Data/VideosTemp.json")