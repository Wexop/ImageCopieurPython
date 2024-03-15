from pynput.mouse import Listener

posTab = []
nbColors = 6


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
