from fileinput import filename
from re import T
from unittest.mock import seal
from venv import create
from xml.etree.ElementTree import TreeBuilder

from matplotlib import colors

import color_functions as cf
import image_functions as imf
from PIL import Image
import math
import block_reader
import color_functions as cf
import create_minecraft_file
import os
import csv


def simplify_wrapper(colors, distance_func=cf.color_distance_redmean_fast):
    def simplify(coordinates, color): 
        return cf.find_closest_color(color, colors, distance_func=distance_func)

    return simplify


# tredje går inte att nå. TROR att den börjar på 1, för att 0 ska vara mörkare och 2 ljusare

def change_colors_by_id(colors, id):
    multipliers = {0: 180, 1: 220, 2: 255, 3: 135}
    multiplier = multipliers[id] / 255

    new_dict = dict()

    for (key, value) in colors.items():
        r, g, b = key
        r = math.floor(r * multiplier)
        g = math.floor(g * multiplier)
        b = math.floor(b * multiplier)

        if not (r, g, b) in new_dict:
            new_dict[(r, g, b)] = (value, id)

        # ELSE, REPLACE IF CHEAPER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    return new_dict



def get_only_colors(colors_dict):
    colors = []

    for (key, values) in colors_dict.items():
        colors.append(key)
    
    return colors


def merge_dicts(dict1, dict2):
    new_dict = dict(dict1)

    for (key, value) in dict2.items():
        if not key in dict1:
            new_dict[key] = value
        else:
            print("COLLISION")
            print(key)
            print(value)
            print(dict1[key])
            print()
    
    return new_dict

# Lägg till för större maps?
def get_map_start_block_from_coordinate(coordinate, height=100):
    x, y, z = tuple(coordinate)
    x = (x - (-64)) // 128 * 128 - 64
    y = height
    z = (z - (-64)) // 128 * 128 - 64
    return (x, y, z)


def blocks_used_in_mcfunction(file):
    with open(file) as f:
        lines = f.readlines()
        blocks = dict()

        for line in lines:
            if not line[:4] == "fill":
                block = line.split(" ")[4][:-1]

                if block in blocks:
                    blocks[block] = blocks[block] + 1
                else:
                    blocks[block] = 1
        
        blocks_2 = []
        for (key,  value) in blocks.items():
            blocks_2.append((key, value))

        blocks_2.sort(key=lambda x: x[1], reverse=True)

        return blocks_2


def differnce_in_block_types(first, second, path):

    a_name = first
    b_name = second

    a = blocks_used_in_mcfunction(path + a_name + ".mcfunction")
    b = blocks_used_in_mcfunction(path + b_name + ".mcfunction")
    c = []

    for x in a:
        if not x in b:
            c.append(x)

    return c


def split_func_file(file_name, number_of_splits, path):
    with open(path + file_name + ".mcfunction", "r") as f:
        lines = f.readlines()
    
    os.remove(path + file_name + ".mcfunction")
    os.mkdir(path + file_name)

    length = math.ceil((len(lines) - 1) / number_of_splits)
    max_length = len(lines)
    j = 0

    for i in range(number_of_splits):
        new_file = path + file_name + "/f" + str(i + 1) + ".mcfunction"

        with open(new_file, "w") as new_f:
            for k in range(length):
                if j == max_length:
                    break
                else:
                    new_f.write(lines[j])
                    j += 1


def display_images(image, map_width=1, map_height=1):
    block_colors_cheap = {
            (255, 255, 255): "white-wool-or-glazed",
            (216, 127, 51): "orange-wool-or-glazed-or-terra",
            (178, 76, 216): "magenta-wool-or-glazed",
            (102, 153, 216): "light-blue-wool-or-glazed",
            (229, 229, 51): "yellow-wool-or-glazed",
            (127, 204, 25): "lime-wool-or-glazed",
            (242, 127, 165): "pink-wool-or-glazed",
            (76, 76, 76): "gray-wool-or-glazed",
            (153, 153, 153): "light-gray-wool-or-glazed",
            (76, 127, 153): "cyan-wool-or-glazed",
            (127, 63, 178): "purple-wool-or-glazed",
            (51, 76, 178): "blue-wool-or-glazed",
            (102, 76, 51): "brown-wool-or-glazed",
            (102, 127, 51): "green-wool-or-glazed",
            (153, 51, 51): "red-wool-or-glazed",
            (25, 25, 25): "black-wool-or-glazed",
            (209, 177, 161): "white-terra",
            (159, 82, 36): "orange-terra",
            (149, 87, 108): "magenta-terra",
            (112, 108, 138): "light-blue-terra",
            (186, 133, 36): "yellow-terra",
            (103, 117, 53): "lime-terra",
            (160, 77, 78): "pink-terra",
            (57, 41, 35): "gray-terra",
            (135, 107, 98): "light-gray-terra",
            (87, 92, 92): "cyan-terra",
            (122, 73, 88): "purple-terra",
            (76, 62, 92): "blue-terra",
            (76, 50, 35): "brown-terra",
            (76, 82, 42): "green-terra",
            (142, 60, 46): "red-terra",
            (37, 22, 16): "black-terra",
            }


    block_colors_cheap = block_reader.read_blocks("palettes/blocks_palette_cheap.txt")
    block_colors_expensive = block_reader.read_blocks("palettes/blocks_palette_all.txt")

    dict_0 = change_colors_by_id(block_colors_cheap, 0)
    dict_1 = change_colors_by_id(block_colors_cheap, 1) # Tror detta är den vanliga
    dict_2 = change_colors_by_id(block_colors_cheap, 2) # 255:an
    dict_3 = change_colors_by_id(block_colors_cheap, 3) # Går endast med verktyg


    # I VILKEN ORDNING SKA DE SLÅS IHOP????????????????
    all_dicts = dict_0 | dict_1
    all_dicts = all_dicts | dict_2
    #all_dicts = all_dicts | dict_3


    dict_0_expensive = change_colors_by_id(block_colors_expensive, 0)
    dict_1_expensive = change_colors_by_id(block_colors_expensive, 1) # Tror detta är den vanliga
    dict_2_expensive = change_colors_by_id(block_colors_expensive, 2) # 255:an
    dict_3_expensive = change_colors_by_id(block_colors_expensive, 3) # Går endast med verktyg


    # I VILKEN ORDNING SKA DE SLÅS IHOP????????????????
    all_dicts_expensive = dict_0_expensive | dict_1_expensive
    all_dicts_expensive = all_dicts_expensive | dict_2_expensive
    #all_dicts_expensive = all_dicts_expensive | dict_3_expensive

    #print(all_dicts_expensive)


    #all_dicts_expensive = merge_dicts(dict_0_expensive, dict_1_expensive)
    #all_dicts_expensive = merge_dicts(all_dicts_expensive, dict_2_expensive)


    colors_all_dicts = get_only_colors(all_dicts)
    func_dicts_all = simplify_wrapper(colors_all_dicts)

    colors2 = get_only_colors(dict_1)
    func_dict_1 = simplify_wrapper(colors2)


    colors_all_dicts_expensive = get_only_colors(all_dicts_expensive)
    func_dicts_all_expensive = simplify_wrapper(colors_all_dicts_expensive)

    colors2_expensive = get_only_colors(dict_1_expensive)
    func_dict_1_expensive = simplify_wrapper(colors2_expensive)


    im1 = Image.open("map_images/" + image)

    im2 = im1.copy()
    im2 = im2.resize((map_width * 128, map_height * 128))

    im3 = im2.copy()
    im3 = imf.apply_func(im3, func_dict_1)
    im3.save("images/costa_rica_simplified.png")

    im4 = im2.copy()
    im4 = imf.apply_func(im4, func_dicts_all)
    im4.save("images/costa_rica_simplified.png")

    im5 = im2.copy()
    im5 = imf.apply_func(im5, func_dict_1_expensive)
    im5.save("images/costa_rica_simplified.png")

    im6 = im2.copy()
    im6 = imf.apply_func(im6, func_dicts_all_expensive)
    im6.save("images/final.png")
    # SPARA SOM VAD????

    all_dicts_expensive_illegal = all_dicts_expensive | dict_3_expensive
    colors_all_dicts_expensive_illegal = get_only_colors(all_dicts_expensive_illegal)
    func_dicts_all_expensive_illegal = simplify_wrapper(colors_all_dicts_expensive_illegal, distance_func=cf.color_distance_euclidean)
    im7 = im2.copy()
    im7 = imf.apply_func(im7, func_dicts_all_expensive_illegal)
    im7.save("images/costa_rica_simplified.png")

    func_dicts_all_expensive_illegal = simplify_wrapper(colors_all_dicts_expensive_illegal)
    im8 = im2.copy()
    im8 = imf.apply_func(im8, func_dicts_all_expensive_illegal)
    im8.save("images/costa_rica_simplified.png")

    images = [im1, im2, im3, im4, im5, im6, im7, im8]
    image_names = ["normal", "converted to " + str(map_width * 128) + "x" + str(map_height * 128), "cheap-blocks-flat", "cheap-blocks-stair", "all-blocks-flat", "all-blocks-stair", "all-blocks-stair-illegal-euclid", "all-blocks-stair-illegal"]
    imf.show_images(images, image_names, 4, 2, save=True, save_name="images/costa_rica_simplified_all.png")




def create_palette_from_custom_palette_file(file_name, palette_of_all_blocks="palettes/blocks_palette_all.txt", sort_for_cheap=True):
    def strip(line):
        if line[-1:] == "\n":
            return line[:-1]
        else:
            return line

    my_palette = []
    with open("custom_palettes/" + file_name + ".txt") as f:
        my_palette = list(map(strip, f.readlines()))
    
    all_blocks = []
    with open(palette_of_all_blocks) as f:
        all_blocks = list(map(strip, f.readlines()))

    final = dict()

    for i in range(0, len(all_blocks), 2):
        #print(all_blocks[i + 1].split(", "))
        final[tuple(all_blocks[i + 1].split(", "))] = tuple(map(lambda x: int(x), all_blocks[i].split(", ")))
    
    out = dict()

    for block in my_palette:

        in_dict = False

        for key, value in final.items():
            if block in key:
                in_dict = True

                if value in out:
                    tmp = out[value]
                    tmp.append(block)
                    out[value] = tmp
                else:
                    out[value] = [block]

                break
        
        if not in_dict:
            print('WARNING: "' + block + '" is not a valid block to choose from')

        #print(str(in_dict) + " " + block)
    
    #print(final)

    if sort_for_cheap:
        out = sort_for_cheapest(out)

    colors = []
    blocks = []

    for key, values in out.items():
        colors.append(key)
        blocks.append(values)
    
    block_reader.save_to_file(colors, blocks, name=file_name)


def create_custom_palette_from_shop_blocks(name, do_price_limit=False, price_limit=15):
    blocks = dict()

    with open("block_data/shop_blocks.csv") as f:
        lines = csv.reader(f)

        for line in lines:
            if not (do_price_limit and float(line[1].replace(",", ".")) > float(price_limit)):
                blocks[line[0].title()] = float(line[1].replace(",", "."))

    # print("hej")
    # print(blocks)

    with open("custom_palettes/" + name + ".txt", "w") as f:

        for block in blocks:
            f.write(block + "\n")


def get_block_prices():
    blocks = dict()

    with open("block_data/shop_blocks.csv") as f:
        lines = csv.reader(f)

        for line in lines:

            blocks[line[0].title()] = float(line[1].replace(",", "."))
    
    return blocks


def sort_for_cheapest(colors):
    block_prices = get_block_prices()
    #colors = block_reader.read_blocks("palettes/" + palette_done + ".txt")

    new_colors = dict()

    for color, blocks in colors.items():
        blocks_with_prices = []
        new_order = []

        for block in blocks:
            blocks_with_prices.append((block, block_prices[block]))
        
        blocks_with_prices.sort(key=lambda x: x[1])

        for item in blocks_with_prices:
            new_order.append(item[0])
        
        new_colors[color] = new_order
    

    return new_colors


def print_used_blocks_nicely(name, path):
    q = blocks_used_in_mcfunction(path + name + ".mcfunction")
    print()
    for (a, b) in q:
        print(str(b) + " " + a[10:])

def get_number_of_different_blocks(name, path):
    return len(blocks_used_in_mcfunction(path + name + ".mcfunction"))

def calculate_price_of_painting(name, path):
    q = blocks_used_in_mcfunction(path + name + ".mcfunction")
    prices = get_block_prices()
    price = 0

    for items in q:
        block = items[0][10:].replace("_", " ").title()
        number = items[1]
        price += prices[block] * number

    return round(price, 5)


def get_map(file_name, block_palette, command_output_name, stair, coordinate_in_zone, map_width=1, map_height=1, show_image=False, height=100, centralize=False, border_block="White Terracotta", distance_func=cf.color_distance_redmean_fast, print_difference=False, remove_blocks=False, func_path="commands/"):

    start_block = get_map_start_block_from_coordinate(coordinate_in_zone, height=height)

    palette = "palettes/" + block_palette + ".txt"
    block_colors = block_reader.read_blocks(palette)

    dict_0 = change_colors_by_id(block_colors, 0)
    dict_1 = change_colors_by_id(block_colors, 1)
    dict_2 = change_colors_by_id(block_colors, 2)

    if stair:
        all_dicts = dict_0 | dict_1
        all_dicts = all_dicts | dict_2
    else:
        all_dicts = dict_1 # TROR ATT DET HÄR ÄR RÄTT FÄRG FÖR PLATT!!!!!!

    #print(all_dicts)

    colors_all_dicts = get_only_colors(all_dicts)
    func_dicts_all = simplify_wrapper(colors_all_dicts, distance_func=distance_func)

    #image_file = "tmp_images/" + file_name.split("/")[-1]
    image_file = "tmp_images/" + file_name

    im1 = Image.open("map_images/" + file_name)
    im1 = im1.resize((map_width * 128, map_height * 128))

    im2 = im1.copy()
    im2 = imf.apply_func(im2, func_dicts_all)
    im2.save(image_file)

    create_minecraft_file.create_file(image_file, palette, func_path + command_output_name + ".mcfunction", start_block, map_width=map_width, map_height=map_height, centralize=centralize, height=height, border_block=border_block, print_difference=print_difference, remove_blocks=remove_blocks)

    if show_image:
        images = [im1, im2]
        image_names = ["Converted to " + str(map_width * 128) + "x" + str(map_height * 128), block_palette + " (stair = " + str(stair) + ")"]
        imf.show_images(images, image_names, 2, 1)
    

def main():

    pal_name = "shop_blocks_all_price600"

    create_custom_palette_from_shop_blocks(pal_name, do_price_limit=True, price_limit=600)

    create_palette_from_custom_palette_file("shop_blocks_all_price600")


    # pal_name = "shop_blocks_all"
    # create_custom_palette_from_shop_blocks(pal_name, do_price_limit=False, price_limit=15)
    # create_palette_from_custom_palette_file("shop_blocks_all")


    coordinate_in_zone = (7000, 200, 7000)
    stair = False
    centralize = True
    start_height = 50
    remove = True
    width = 1
    height = 1

    display = False
    picture = "hip_dog.png"
    #palette = "blocks_palette_all"
    palette = "shop_blocks_all_price600"
    name = "dog4"

    split_file = False
    number_of_splits = 1

    #path = "commands/"
    path = "C:\\Users\\Hampus\\AppData\\Roaming\\.minecraft\\saves\\Second Map Art\\datapacks\\MapBot\\data\\mapbot\\functions\\"
    override = False
    color_func = cf.color_distance_redmean_fast
    #color_func = cf.color_distance_euclidean



    if not override:
        if display:
            display_images(picture, map_width=width, map_height=height)

        else:
            get_map(picture, palette, name, stair, coordinate_in_zone, map_width=width, map_height=height, show_image=True, height=start_height, centralize=centralize, border_block="White Terracotta", distance_func=color_func, print_difference=True, remove_blocks=remove, func_path=path)

            if split_file:
                split_func_file(name, number_of_splits, path)
    
    #print(differnce_in_block_types("new11", "new10", path))


    print_used_blocks_nicely(name, path)
    print()
    print("Number of different blocks: " + str(get_number_of_different_blocks(name, path)))
    print()
    print("Price: " + str(calculate_price_of_painting(name, path)))
    

if __name__ == "__main__":
    main()