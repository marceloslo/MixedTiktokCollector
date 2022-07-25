import pandas as pd
import json
import urllib
from ExtractText import Extract
from Transcribe import Transcribe
import os

def write_document_to_file(document, file):
    json.dump(document, file)
    file.write("\n")
    file.flush()

def Collect(tempMp4=True):
    videosMetadata = pd.read_json("../../Data/VideoMetadata.json",lines=True)
    videosMetadata = videosMetadata.to_dict('records')


    invalid_characters = ['/','\\',':','*','?','<','>','|','\"']

    transcriptions = []
    count = 0
    for line in videosMetadata:
        src = line['Content']
        if src == "":
            continue
        url = line['Url']
        filename = line['Url']
        for char in invalid_characters:
                filename = filename.replace(char,'')
        try:
            path = 'D:/TikTokMp4/'+filename+'.mp4'
            urllib.request.urlretrieve(src, path)
            transcription = Transcribe(path,url)
            print("Transcription done for:",url)
            transcription['Text'] = Extract(path)
            print("Extraction done for:",url)
            transcriptions.append(transcription)
            if tempMp4:
                os.remove(path)
            count+=1
        except:
            print("Failed to download video: ",url)
            continue
        if count%100 == 0:
            with open('../../Data/Transcripts.json','a', encoding='utf-8') as file:
                for line in transcriptions:
                    write_document_to_file(line,file)
            count=0
            transcriptions=[]

    if len(transcriptions) > 0:
        with open('../../Data/Transcripts.json','a', encoding='utf-8') as file:
            for line in transcriptions:
                write_document_to_file(line,file)

if __name__ == "__main__":
    Collect()
