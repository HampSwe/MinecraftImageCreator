import pyautogui as ag
import time

ag.hotkey("win", "r")
time.sleep(0.5)
ag.write("cmd", interval=0.1)
time.sleep(0.5)
ag.press("enter")
time.sleep(0.5)
ag.write("Hello there", interval=0.1)