import random
import time
from io import BytesIO

import keyboard
import pyautogui
import requests
from PIL import Image
from pyautogui import keyDown
from pynput.mouse import Listener

# Récupérer les entrées utilisateur
randomTab = input("random ? y/n : ")
imageUrl = input("Url de l'image : ")
average = int(input("Moyenne de rgb pour le noir : "))
rescale = int(input("Rescale l'image : "))
waitClick = input('Attendre un click ? y/n : ')
clicked = False

# Télécharger et préparer l'image
image = requests.get(imageUrl, stream=True)
finalImage = BytesIO(image.content)
image = Image.open(finalImage).reduce(rescale)
width, height = image.size

# Position de départ initiale
startX, startY = 546, 316

minLineLen = 10
minBetweenLineLen = 20

# Classe pour gérer le clic de la souris
class ClickListener:
    def __init__(self):
        self.clicked = False
        self.startX = startX
        self.startY = startY

    def on_click(self, x, y, button, pressed):
        if pressed and not self.clicked:
            self.clicked = True
            self.startX, self.startY = pyautogui.position()
            print("CLICKED")
            return False

# Attendre un clic si nécessaire
listener = ClickListener()
if waitClick == "y":
    with Listener(on_click=listener.on_click) as l:
        l.join()
    startX, startY = listener.startX, listener.startY

# Fonction pour obtenir la moyenne RGB pour la luminosité du pixel
def get_rgb_average(rgb_tuple):
    return sum(rgb_tuple[:3]) / 3

# Préparer les lignes à dessiner
drawTab = []
for y in range(height):
    line = None
    for x in range(width):
        pixel = image.getpixel((x, y))
        avg = get_rgb_average(pixel)
        is_black = avg < average

        if is_black:
            if not line:
                line = [y, x, x]  # Commence une nouvelle ligne
            else:
                line[2] = x  # Étend la ligne jusqu'à la position x actuelle
        else:
            if line:
                drawTab.append(line)
                line = None
    if line:
        drawTab.append(line)  # Ajoute la ligne restante à la fin de la ligne

# Supprimer les lignes de moins de 5 pixels
drawTab = [line for line in drawTab if (line[2] - line[1]) >= minLineLen]

# Fusionner les lignes séparées par moins de 5 pixels
optimizedTab = []
if drawTab:
    current_line = drawTab[0]
    for line in drawTab[1:]:
        # Si la ligne actuelle et la suivante sont sur la même ligne et proches, fusionne-les
        if line[0] == current_line[0] and line[1] - current_line[2] <= minBetweenLineLen:
            current_line[2] = line[2]  # Étend la fin de la ligne actuelle
        else:
            optimizedTab.append(current_line)
            current_line = line
    optimizedTab.append(current_line)  # Ajoute la dernière ligne traitée

drawTab = optimizedTab

print('LONGUEUR DE DRAW TAB =', len(drawTab))
print('DURÉE ESTIMÉE DU DESSIN =', len(drawTab) * 0.21835443037974683544303797468354, "SECONDES")

# Mélanger les lignes si nécessaire
if randomTab == 'y':
    random.shuffle(drawTab)

# Dessiner les lignes avec pyautogui
time.sleep(1)
start_time = time.time()  # Temps de début

for y, start_x, end_x in drawTab:
    if keyboard.is_pressed('e'):
        print("La touche 'E' a été appuyée, arrêt de la boucle.")
        break
    x = startX + start_x
    y = startY + y
    endX = startX + end_x
    pyautogui.moveTo(x, y, 0)
    pyautogui.dragTo(endX)

end_time = time.time()  # Temps de fin
duration = end_time - start_time

# Afficher la durée totale de l'exécution de la boucle de dessin
print('Durée totale de la boucle de dessin :', duration, 'secondes')
