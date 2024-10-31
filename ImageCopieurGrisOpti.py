import random
import time
from io import BytesIO
from operator import itemgetter

import keyboard
import pyautogui
import requests
from PIL.Image import open as openImage
from pynput.mouse import Listener

startX = 546
startY = 316

# Chargement des positions depuis le fichier de configuration
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

# Positions des couleurs et outils
posGrey1 = posTab[0]
posGrey2 = posTab[1]
posGrey3 = posTab[2]
posGrey4 = posTab[3]
posGrey5 = posTab[4]
posGrey6 = posTab[5]

posColor1 = posTab[6]
posColor2 = posTab[7]
posRect = posTab[8]
posPen = posTab[9]


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


def selectColor(color):
    # Cliquer sur color1, puis sur la couleur choisie
    pyautogui.click(posColor1[0], posColor1[1])  # Clique sur color1
    if color == 1:
        pyautogui.click(posGrey1[0], posGrey1[1])
    elif color == 2:
        pyautogui.click(posGrey2[0], posGrey2[1])
    elif color == 3:
        pyautogui.click(posGrey3[0], posGrey3[1])
    elif color == 4:
        pyautogui.click(posGrey4[0], posGrey4[1])
    elif color == 5:
        pyautogui.click(posGrey5[0], posGrey5[1])
    else:
        pyautogui.click(posGrey6[0], posGrey6[1])

    # Cliquer sur color2, puis sur la couleur choisie
    pyautogui.click(posColor2[0], posColor2[1])  # Clique sur color2
    if color == 1:
        pyautogui.click(posGrey1[0], posGrey1[1])
    elif color == 2:
        pyautogui.click(posGrey2[0], posGrey2[1])
    elif color == 3:
        pyautogui.click(posGrey3[0], posGrey3[1])
    elif color == 4:
        pyautogui.click(posGrey4[0], posGrey4[1])
    elif color == 5:
        pyautogui.click(posGrey5[0], posGrey5[1])
    else:
        pyautogui.click(posGrey6[0], posGrey6[1])


time.sleep(1)

rectangles = []  # Liste des rectangles à dessiner
taken_pixels = set()  # Ensemble pour suivre les pixels déjà utilisés

for y in range(hauteur):
    x = 0
    while x < largeur:
        pixel = i.getpixel((x, y))
        avg = getRgbAverage(pixel)
        color = pixelColor(avg)

        if color != 1:  # Ignorer les pixels blancs
            start_x = x

            # Trouver la largeur du rectangle
            while x < largeur and pixelColor(getRgbAverage(i.getpixel((x, y)))) == color:
                x += 1

            end_x = x - 1  # La dernière position x de ce rectangle

            # Vérifier si ce rectangle chevauche des pixels déjà utilisés
            can_draw = True
            for check_x in range(start_x, end_x + 1):
                if (check_x, y) in taken_pixels:
                    can_draw = False  # Ne pas dessiner si overlap
                    break

            if can_draw:  # Si le rectangle n'a pas chevauché, l'ajouter
                # Déterminer la hauteur du rectangle
                rect_height = 1
                while y + rect_height < hauteur and all(
                        (check_x, y + rect_height) not in taken_pixels for check_x in range(start_x, end_x + 1)
                ):
                    rect_height += 1

                if rect_height > 1:  # S'assurer d'avoir une hauteur valide
                    rectangles.append([y, start_x, end_x, color, rect_height])
                    for check_x in range(start_x, end_x + 1):
                        for h in range(y, y + rect_height):
                            taken_pixels.add((check_x, h))  # Marquer les pixels comme pris
        x += 1

# Filtrer pour obtenir uniquement les grands rectangles (40 pixels de large minimum)
filtered_rectangles = [r for r in rectangles if r[2] - r[1] >= 40]

# Randomiser et trier si nécessaire
if randomTab == 'y':
    random.shuffle(filtered_rectangles)

filtered_rectangles.sort(key=itemgetter(3))

print('LONGUEUR DE DRAW TAB =', len(filtered_rectangles))
print('DURÉE ESTIMÉE DU DESSIN =', len(filtered_rectangles) * 0.06283084004602991944764096662831, "SECONDES")

pyautogui.PAUSE = 0.01
start_time = time.time()  # Temps de début

lastcolor = None  # Variable pour garder la trace de la dernière couleur utilisée

for rect in filtered_rectangles:
    if keyboard.is_pressed('space'):
        print("La touche 'space' a été appuyée, arrêt de la boucle.")
        break

    y = startY + rect[0]
    start_x = startX + rect[1]
    end_x = startX + rect[2]
    color = rect[3]
    rect_height = rect[4]  # Hauteur du rectangle

    # Sélectionner la couleur si elle a changé
    if color != lastcolor:
        selectColor(color)
        lastcolor = color

    # Dessiner le rectangle
    pyautogui.click(posRect[0], posRect[1])  # Sélectionner l'outil rectangle
    pyautogui.moveTo(start_x, y)
    pyautogui.mouseDown()
    pyautogui.dragTo(end_x, y + rect_height)  # Dessiner le rectangle avec la hauteur
    pyautogui.mouseUp()

    # Décalage pour le prochain rectangle
    pyautogui.moveTo(end_x + 10, y)
    pyautogui.mouseDown()
    pyautogui.mouseUp()

end_time = time.time()  # Temps de fin
duration = end_time - start_time

# Afficher la durée totale de l'exécution de la boucle de dessin
print('Durée totale de la boucle de dessin :', duration, 'secondes')
