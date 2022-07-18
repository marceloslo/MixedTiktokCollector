import speech_recognition as sr 
import moviepy.editor as mp
import json
import os

def write_document_to_file(document, file):
    json.dump(document, file,ensure_ascii = False)
    file.write("\n")
    file.flush()

videoname = "httpswww.tiktok.com@bolsonaromessiasjairvideo7063796844056349958.mp4"

def transcribe(videoname):
    clip = mp.VideoFileClip("D:/TikTokMp4/"+videoname) 
    
    clip.audio.write_audiofile("temp.wav")

    r = sr.Recognizer()

    audio = sr.AudioFile("temp.wav")

    with audio as source:
        r.adjust_for_ambient_noise(source)
        audio_file = r.record(source)
        result = r.recognize_google(audio_file,language = 'pt-PT',show_all=True)

    final = {'Source':videoname.replace('.mp4',''),'Transcript':result['alternative'][0]['transcript']}

    print(final)

    # exporting the result 
    with open('../../Data/transcripts.json','a',encoding='utf-8') as file: 
        write_document_to_file(final,file)
    
    os.remove("temp.wav")

transcribe(videoname)