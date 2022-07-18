import cv2
import pytesseract
import re

path = "D:/TikTokMp4/httpswww.tiktok.com@bolsonaromessiasjairvideo7063796844056349958.mp4"

vidcap = cv2.VideoCapture(path)
success,frame = vidcap.read()
framenbr = 0
print(pytesseract.get_languages(config=''))

dataold =''
while success:
    success,frame = vidcap.read()
    if not success:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    blr = cv2.GaussianBlur(gray, (3, 3), 0)
    gray = cv2.threshold(blr, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    data = pytesseract.image_to_string(gray, lang='por', config='--psm 12').lower()
    data = re.sub('[^A-Za-z0-9çáéíóúàãõ@ \n]+', '', data)
    data = re.sub('[^A-Za-z0-9çáéíóúàãõ@ ]+', ' ', data)
    if dataold != data:
        print(data + '\nFrame number: ' + str(framenbr))
    dataold=data
    framenbr += 1