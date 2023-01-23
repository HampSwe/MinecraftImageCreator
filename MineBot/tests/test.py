from email.policy import default
from turtle import screensize
import pyautogui as ag
import playsound
import keyboard
import time
from image_detect import find_image
import image_names
#import pydirectinput as di



# https://pypi.org/project/PyDirectInput/



# Python 3.10.2
# pip install pyautogui
# pip install pillow
# pip install opencv-python
# pip install numpy
# pip install keyboard
# OPTIONAL: pip install playsound
# OPTIONAL: pip install pydirectinput

# p_ = 0
# p = 0

# while True:
#     p = ag.position()

#     if not p == p_:
#         p_ = p
#         print(p)




#size = ag.size()
#print(size)

#center_x = size[0] // 2
#center_y = size[1] // 2


# ag.moveTo(center_x, center_y)
# ag.moveRel(300, 300, 1, ag.easeInOutQuad)

# time.sleep(1)

# ag.moveTo(center_x, center_y)
# ag.moveRel(300, 300, 1, ag.easeInQuad)

# time.sleep(1)

# ag.moveTo(center_x, center_y)
# ag.moveRel(300, 300, 1, ag.easeOutQuad)





# ag.moveTo(center_x, center_y - 200)

# ag.click()

# ag.mouseDown()

# ag.move(0, 200, 1, ag.easeInOutQuad)

# ag.mouseUp()

# ag.moveTo(1000, 555)
# ag.click()

# time.sleep(1)

# ag.write("Hello", interval=0.05)



# ag.hotkey("win", "r")
# time.sleep(0.5)
# ag.write("cmd", interval=0.1)
# time.sleep(0.5)
# ag.press("enter")
# time.sleep(0.5)
# ag.write("echo " + "Hello there", interval=0.1)
# time.sleep(0.1)
# ag.press("enter")




# ag.alert(text='Hejsan', title='MineBot', button='OK')
# ag.confirm(text='Hejsan', title='MineBot', buttons=['OK', 'Cancel'])
# text = ag.prompt(text='Hej', title='MineBot', default='')

# print(text)



# time.sleep(5)
# ag.screenshot("start.png")


#playsound.playsound("complete.mp3")



# def click_image_old(image_name, confidence=1, smooth=False):
#     if confidence == 1:
#         button = ag.locateCenterOnScreen(image_name)

#     else:
#         button = ag.locateCenterOnScreen(image_name, confidence=confidence)
    
#     if not button is None:
#         if smooth:
#             ag.dragTo(x=button.x, y=button.y, duration=0.8, tween=ag.easeInOutQuad)
#             time.sleep(0.5)
#             ag.click()
#         else:
#             ag.moveTo(x=button.x, y=button.y)
#             ag.click()
#     else:
#         print("Could not find " + image_name)
#         return False
    
#     return True


# def click_image_repeatedly_old(image_name, times, confidence=1, smooth=False):
#     for i in range(times):
#         if click_image(image_name, confidence=confidence, smooth=smooth):
#             return True

#         time.sleep(0.1)

#     return False



# screen = ag.screenshot("screenshot.png")

# a = find_image("screenshot.png", "multiplayer_button.png")
# print(a)

# a = click_image_repeatedly("multiplayer_button.png", 5, confidence=0.9, smooth=True)
# print(a)
# print(ag.position())

# di.keyDown("w")
# time.sleep(3)
# di.keyUp("w")

# def main():
#     while True:
#         # wait_for_keypress("q")
#         # click_image(images.MULTIPLAYER_BUTTON, smooth=True, mouse_hide=True)
#         # time.sleep(0.5)

#         wait_for_keypress("q")
#         click_image(images.MULTIPLAYER_BUTTON, smooth=False, mouse_hide=True)
#         time.sleep(0.5)


def wait_for_keypress(key, sleep_time=0.25):

    print("Press '" + key + "' to start the bot")

    while True:
        if keyboard.is_pressed(key):
            break

    time.sleep(sleep_time)


def click_image(image_name, smooth=False, mouse_hide=True):

    if mouse_hide:
        last_x, last_y = ag.position()
        ag.moveTo(1, 1)

    ag.screenshot("images/screenshot.png")
    x, y = find_image("images/screenshot.png", image_name)
    
    if mouse_hide:
        ag.moveTo(last_x, last_y)

    if smooth:
        ag.moveTo(x=x, y=y, duration=0.8, tween=ag.easeInOutQuad)
        time.sleep(0.5)
        ag.click()
    else:
        ag.moveTo(x=x, y=y)
        ag.click()


def start_minecraft():

    time.sleep(0.5)
    ag.hotkey("win", "d")

    time.sleep(0.5)
    click_image(image_names.MINECRAFT_LOGO)
    ag.click()

    time.sleep(4)
    click_image(image_names.SPELA, smooth=True, mouse_hide=False)

    time.sleep(18)
    click_image(image_names.MAXIMIZE, smooth=True, mouse_hide=False)

    # time.sleep(1)
    # click_image(images.SINGLEPLAYER_BUTTON, smooth=True, mouse_hide=False)





def main():

        start_minecraft()

        wait_for_keypress("q")

        # click_image(images.SINGLEPLAYER_BUTTON, smooth=False, mouse_hide=True)
        # time.sleep(0.5)


        # keyboard.press("w")
        # time.sleep(3)
        # keyboard.release("w")

        # keyboard.press_and_release("esc")


if __name__ == "__main__":
    main()



# time.sleep(5)
# di.press("f11")
# time.sleep(5)


# time.sleep(5)
# di.keyDown("w")
# time.sleep(5)
# di.keyUp("w")

#playsound.playsound("complete.mp3")




