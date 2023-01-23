from email.policy import default
from tracemalloc import start
from turtle import screensize

from pyparsing import opAssoc
from image_detect import find_image
import pyautogui as ag
import playsound
import keyboard
import time
import image_names
import number_program
import math


class GUI:
    @classmethod
    def wait_for_keypress(self, key, sleep_time=0.25):
        print("Press '" + key + "' to start the bot")

        while True:
            if keyboard.is_pressed(key):
                break

        time.sleep(sleep_time)
    
    @classmethod
    def write_text(self, text):
        for c in text:
            if c in [":", "_", "/"]:
                keyboard.press("shift")
                keyboard.press_and_release(c)
                keyboard.release("shift")
            else:
                keyboard.press_and_release(c)


    # @classmethod
    # def write_text(self, text, duration=0.1):
    #     for c in text:
    #         keyboard.press_and_release(c)
    #         time.sleep(duration)

    @classmethod
    def start_minecraft(self):
        time.sleep(0.5)
        ag.hotkey("win", "d")

        time.sleep(0.5)
        GUI.click_image(image_names.MINECRAFT_LOGO)
        ag.click()

        time.sleep(4+5)
        GUI.click_image(image_names.SPELA, smooth=True, mouse_hide=False)

        time.sleep(18)
        GUI.click_image(image_names.MAXIMIZE, smooth=True, mouse_hide=False)


    @classmethod
    def click_image(self, image_name, smooth=False, mouse_hide=True):

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



class Bot:
    def __init__(self, manual_start=False, start_key="i", start_with_key=True, system="windows", gui_value=3, gui_margin=23):
        self.manual_start = False
        self.start_key = start_key
        self.start_with_key = start_with_key
        self.system = system
        self.gui_value = gui_value
        self.gui_margin = gui_margin
    
        if manual_start:
            GUI.start_minecraft()
        
        if start_with_key:
            GUI.wait_for_keypress(start_key)
        
        if system == "windows":
            self.coo_box_start = (74, 296)
            self.coo_box_end = (615, 323)


    def join_singleplayer_world(self, world_icon):
        time.sleep(1)
        self.singleplayer_start()
        time.sleep(1.5)
        GUI.click_image(world_icon)

    def join_multiplayer_world(self, world_icon):
        time.sleep(1)
        self.multiplayer_start()
        time.sleep(1.5)
        GUI.click_image(world_icon)

    def singleplayer_start(self):
        GUI.click_image(image_names.SINGLEPLAYER_BUTTON, smooth=False, mouse_hide=True)

    def multiplayer_start(self):
        GUI.click_image(image_names.MULTIPLAYER_BUTTON, smooth=False, mouse_hide=True)

    def get_coordinates(self):
        ag.screenshot("images/coordinates.png", region=(self.coo_box_start[0], self.coo_box_start[1], self.coo_box_end[0] - self.coo_box_start[0], self.coo_box_end[1] - self.coo_box_start[1]))

    def get_coordinates(self):
        return number_program.get_coordinates(gui=self.gui_value, margin=self.gui_margin)

    def say_coordinates_and_direction(self):
        coordinates = self.get_coordinates()
        direction = self.get_direction()

        self.say("coordinates: " + str(coordinates[0]) + " " + str(coordinates[1]) + " " + str(coordinates[2]))
        self.say("direction: " + str(direction[0]) + " " + str(direction[1]))

    def get_direction(self):
        return number_program.get_direction(gui=self.gui_value, margin=self.gui_margin)

    def start_bot(self):
        keyboard.press_and_release("f3")
    
    def say(self, text):
        keyboard.press_and_release("enter")
        time.sleep(0.1)
        GUI.write_text(text)
        keyboard.press_and_release("enter")

    def run_command(self, command):
        keyboard.press_and_release("enter")
        time.sleep(0.1)
        GUI.write_text("/" + command)
        keyboard.press_and_release("enter")


    def print_commands_from_file(self, file_name):
        file = "commands/" + file_name + ".mcfunction"

        with open(file) as f:
            commands = f.readlines()
        
        # times = [2, 3, 3, 2, 5]

        # # Fill-kommandosen tar mer tid
        # for i in range(5):
        #     self.run_command(commands[0][:-1])
        #     del commands[0]
        #     time.sleep(times[i])

        # self.run_command(commands[0][:-1])
        # del commands[0]
        # time.sleep(2)
        # self.run_command(commands[0][:-1])
        # del commands[0]
        # time.sleep(2)

        for command in commands:
            if keyboard.is_pressed("q") and keyboard.is_pressed("i"):
                break
            else:
                self.run_command(command[:-1])

                if command[:-1][:4] == "fill":
                    time.sleep(1)

            #time.sleep(0.1)
        
        self.run_command("say done")


    def get_distance_between_cords(self, c1, c2):
        return math.sqrt((c2[0] - c1[0]) ** 2 + (c2[1] - c1[1]) ** 2 + (c2[2] - c1[2]) ** 2)


    def walk_mean(self, duration, n):
        def walk_time_dist(duration):
            coords0 = self.get_coordinates()

            keyboard.press("w")
            time.sleep(duration)
            keyboard.release("w")
            time.sleep(0.5)

            coords1 = self.get_coordinates()
            return self.get_distance_between_cords(coords0, coords1)

        deltas = []
        for i in range(n):
            deltas.append(walk_time_dist(duration))
            time.sleep(0.5)

        #print(deltas)
        sum = 0

        for i in deltas:
            sum += i
        
        mean = sum / len(deltas)

        return mean


    def multiple_means(self, n):

        means = []
        for i in range(5, 50, 5):
            means.append(str(i / 10) + " seconds: " + str(self.walk_mean(i / 10, n)))
        
        for i in means:
            print(i)


def main():
    # bot = Bot(manual_start=True, start_with_key=False)
    # # bot.join_singleplayer_world(image_names.ICON_BOT)
    # bot.join_multiplayer_world(image_names.ICON_COMPLEX)


    # bot.start_bot()
    # bot.get_coordinates()



    bot = Bot(manual_start=False, start_with_key=True, gui_value=3, gui_margin=23)

    #bot.say_coordinates_and_direction()

    # tid = time.time()
    # bot.get_coordinates()
    # print(time.time() - tid)

    keyboard.press("shift")

    print(bot.walk_mean(0.05, 10))

    keyboard.release("shift")

    #bot.multiple_means(3)


    # tid = time.time()
    # bot.print_commands_from_file("commands_test")
    # print(time.time() - tid)



    # for i in range(1000):
    #     bot.run_command("/say {0}".format(i))


if __name__ == "__main__":
    main()