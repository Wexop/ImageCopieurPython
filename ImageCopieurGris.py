import random
import time
from io import BytesIO
from operator import itemgetter

import pyautogui
import requests
from PIL.Image import open as openImage
from pynput.mouse import Listener


startX = 546
startY = 316

f = open("config.txt", "r")
posTab = eval(f.read())
f.close()
print(posTab)
print("BIEN LANCER LE SCRIPT INTICOLORS AVANT UTILISATION")
rescale = int(input("Rescale l'image : "))
randomTab = input("random ? y/n : ")
imageUrl = input("Url de l'image : ")
waitClick = input('Attendre un click ? y/n : ')
clicked = False

image = requests.get(imageUrl, stream=True)
finalImage = BytesIO(image.content)


posGrey1 = posTab[0]
posGrey2 = posTab[1]
posGrey3 = posTab[2]
posGrey4 = posTab[3]
posGrey5 = posTab[4]
posGrey6 = posTab[5]


def on_click(x, y, button, pressed):
    global clicked
    global startY
    global startX
    if not clicked:
        clicked = True
        print("CLICKED x: " + str(x), "y : " + str(y))
        startX = pyautogui.position().x
        startY = pyautogui.position().y
        listener.stop()


with Listener(on_click=on_click) as listener:
    listener.join()

if waitClick == "y":
    while not clicked:
        print('t')

i = openImage(finalImage)
i = i.reduce(rescale)
largeur = i.size[0]
hauteur = i.size[1]

white = 255 * 3


def getRgbAverage(tuple):
    return tuple[0] + tuple[1] + tuple[2]


def pixelColor(number):
    if number <= 109:
        return 6
    elif number <= 218:
        return 5
    elif number <= 327:
        return 4
    elif number <= 436:
        return 3
    elif number <= 545:
        return 3
    elif number <= 654:
        return 2
    else:
        return 1


def selectColor(number):
    if number == 1:
        pyautogui.click(posGrey1[0], posGrey1[1])
    elif number == 2:
        pyautogui.click(posGrey2[0], posGrey2[1])
    elif number == 3:
        pyautogui.click(posGrey3[0], posGrey3[1])
    elif number == 4:
        pyautogui.click(posGrey4[0], posGrey4[1])
    elif number == 5:
        pyautogui.click(posGrey5[0], posGrey5[1])
    else:
        pyautogui.click(posGrey6[0], posGrey6[1])


time.sleep(1)

drawTab = []

for y in range(hauteur):
    line = []
    createLine = True
    lastColor = 1

    for x in range(largeur):
        pixel = i.getpixel((x, y))
        avg = getRgbAverage(pixel)
        color = pixelColor(avg)

        if color == lastColor and color != 1:
            if createLine:
                line = [y, x, x, color]
                createLine = False
            if not createLine:
                line[2] = x
        if color != lastColor:
            lastColor = color
            if len(line) > 0 and not createLine:
                drawTab.append(line)
                line = []
                createLine = True

if randomTab == 'y':
    random.shuffle(drawTab)

drawTab.sort(key=itemgetter(3))

lastcolor = 2
selectColor(lastcolor)

for line in drawTab:
    x = startX + line[1]
    y = startY + line[0]
    endX = startX + line[2]
    color = line[3]
    if color != lastcolor:
        selectColor(color)
        lastcolor = color

    pyautogui.moveTo(x, y, 0)
    pyautogui.mouseDown()
    pyautogui.dragTo(endX, mouseDownUp=True)
    pyautogui.mouseUp()
