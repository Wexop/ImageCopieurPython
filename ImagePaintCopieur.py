import random
import time
from io import BytesIO

import pyautogui
import requests
from PIL.Image import open as openImage
from pynput.mouse import Listener

randomTab = input("random ? y/n : ")
imageUrl = input("Url de l'image : ")
average = int(input("Moyenne de rgb pour le noir : "))
waitClick = input('Attendre un click ? y/n : ')
clicked = False

image = requests.get(imageUrl, stream=True)
finalImage = BytesIO(image.content)

startX = 546
startY = 316


def on_click(x, y, button, pressed):
    global clicked
    global startY
    global startX
    if not clicked:
        clicked = True
        print("CLICKED")
        startX = pyautogui.position().x
        startY = pyautogui.position().y
        listener.stop()


with Listener(on_click=on_click) as listener:
    listener.join()

if waitClick == "y":
    while not clicked:
        print(clicked)

i = openImage(finalImage)
largeur = i.size[0]
hauteur = i.size[1]

white = 255 * 3


def getRgbAverage(tuple):
    return (tuple[0] + tuple[1] + tuple[2]) / 2


def pixelColor(number):
    if number >= average:
        return 0  # white
    else:
        return 1  # black


time.sleep(1)

drawTab = []

for y in range(hauteur):
    line = []
    createLine = True

    for x in range(largeur):
        pixel = i.getpixel((x, y))
        avg = getRgbAverage(pixel)
        color = pixelColor(avg)

        if color == 1:
            if createLine:
                line = [y, x, x]
                createLine = False
            if not createLine:
                line[2] = x
        if color == 0:
            if len(line) > 0 and not createLine:
                drawTab.append(line)
                line = []
                createLine = True

if randomTab == 'y':
    random.shuffle(drawTab)

for line in drawTab:
    x = startX + line[1]
    y = startY + line[0]
    endX = startX + line[2]
    pyautogui.moveTo(x, y, 0)
    pyautogui.dragTo(endX)
