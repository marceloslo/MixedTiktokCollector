import cv2
import pytesseract
import re





def Extract(path):
    with open('words/corpus.txt', 'r', encoding="utf-8") as file:
        palavras = file.read().splitlines()

    palavras=set(palavras)
    vidcap = cv2.VideoCapture(path)
    success,frame = vidcap.read()
    framenumber = 0
    text = []
    while success:
        wordsinvideo = []
        success,frame = vidcap.read()
        framenumber+=1
        if not ((framenumber-1)%30 == 0):
            continue
        if not success:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        blr = cv2.GaussianBlur(gray, (3, 3), 0)
        gray = cv2.threshold(blr, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        data = pytesseract.image_to_string(gray, lang='por', config='--psm 12').lower()
        data = re.sub('[^A-Za-z0-9çáéíóúàãõ@ ]+', ' ', data)
        data = data.lower()
        for i in palavras:
            if i in data:
                wordsinvideo.append(i)
        save = {'Content':wordsinvideo,'Frame':framenumber-1}
        text.append(save)
    return text

if __name__ == '__main__':
    path = "D:/TikTokMp4/httpswww.tiktok.com@bolsonaromessiasjairvideo7063796844056349958.mp4"
    print(Extract(path,'httpswww.tiktok.com@bolsonaromessiasjairvideo7063796844056349958'))