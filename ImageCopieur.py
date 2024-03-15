from PIL.Image import open as openImage

i = openImage("image.png")
largeur = i.size[0]
hauteur = i.size[1]

white = 255 * 3
average = int(input("Moyenne de rgb pour le noir : "))


def getRgbAverage(tuple):
    return (tuple[0] + tuple[1] + tuple[2]) / 2


def pixelColor(number):
    if number >= average:
        return "  "  # white
    else:
        return ". "  # black


string = ""
for y in range(hauteur):
    string += "\n"
    for x in range(largeur):
        pixel = i.getpixel((x, y))
        avg = getRgbAverage(pixel)
        string += pixelColor(avg)

f = open("text.txt", "w")
f.write(string)
f.close()
