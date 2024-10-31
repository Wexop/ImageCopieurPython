from pynput.mouse import Listener

posTab = []
nbColors = 10

#6 premiers => du plus clair au moins clair (255 -51 etc)
#7 pos couleur1
#8 pos couleur2
#9 pos carré
#10 pos crayon


def on_click(x, y, button, pressed):
    if not pressed:
        return
    posTab.append((x, y))
    print(posTab)
    if len(posTab) == nbColors:
        listener.stop()
        save()


def save():
    f = open("config.txt", "w")
    f.write(str(posTab))
    f.close()


with Listener(on_click=on_click) as listener:
    listener.join()
