import pyautogui as ag
import keyboard

p_ = 0
p = 0

while True:
    p = ag.position()

    if not p == p_:
        p_ = p
        print(p)
    
    if keyboard.is_pressed("q"):
        break