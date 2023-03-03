import win32api
import keyboard

position = []

while(True):
    if keyboard.is_pressed('q'):
        break
    else:
        x, y = win32api.GetCursorPos()
        print(x, y)
        position.append([x, y])

print(position)