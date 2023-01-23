from PIL import Image
import pyautogui as ag
import time

NUMBER_0 = "characters/number0.png"
NUMBER_1 = "characters/number1.png"
NUMBER_2 ="characters/number2.png"
NUMBER_3 = "characters/number3.png"
NUMBER_4 ="characters/number4.png"
NUMBER_5 = "characters/number5.png"
NUMBER_6 ="characters/number6.png"
NUMBER_7 = "characters/number7.png"
NUMBER_8 ="characters/number8.png"
NUMBER_9 = "characters/number9.png"
BACKSLASH = "characters/backslash.png"
MINUS = "characters/minus.png"
DOT = "characters/dot.png"
SPACE = "characters/space.png"
OPEN_PARENTHESES = "characters/open_parentheses.png"
CLOSE_PARENTHESES = "characters/close_parentheses.png"


# I princip varje character är 5 enhets-pixlar bred. Spacingen mellan varje karaktär är 1 enhets-pixel bred. På min skärm är 1 enhets-pixel 3 pixlar på skärmen i mc. 

# Koordinaterna måste vara mindre än en 10 000 000 på x resp. z, och mindre än 10 000 på y. Vill du ha mer, öka bredden i enhets-pixelar med 12 för varje decimal
# Bredden för dessa restriktioner är 219 (207) pixelenheter, vilket multipliceras med GUI-värdet för att få bredden i skärmens pixlar
# Den är 7 enhetspixlar hög
# Den börjar 26 enhetspixlar in till höger
# Den börjar 92 enhetspixlar ner, plus antalet skrämpixlar som fönsterkanten är (kallas margin, på min PC 23 pixlar. Windows verkar ha 25 från default?)

#a = (7 + 7 + 4) * 6 + (-1) + 2 * (4 + 6 + 4) + 11*6 + 3*2
#print(a)

def get_characters():
    characters = [(NUMBER_0, "0", 5), (NUMBER_1, "1", 5), (NUMBER_2, "2", 5), (NUMBER_3, "3", 5), (NUMBER_4, "4", 5), (NUMBER_5, "5", 5), (NUMBER_6, "6", 5), (NUMBER_7, "7", 5), (NUMBER_8, "8", 5), (NUMBER_9, "9", 5), (BACKSLASH, "/", 5), (MINUS, "-", 5), (DOT, ".", 1), (SPACE, " ", 3), (OPEN_PARENTHESES, "(", 3), (CLOSE_PARENTHESES, ")", 3)]
    return list(map(lambda x: (convert_to_black_and_white_array(x[0]), x[1], x[2]), characters))


# Färgen på texten är (221, 221, 221)
def convert_to_black_and_white_array(img_input, white_color=(221, 221, 221), black_color=(0, 0, 0)):
    img = Image.open(img_input)
    pixels = img.load()

    w, h = img.width, img.height

    out = []
    tmp = []

    for y in range(h):
        for x in range(w):
            pixel = pixels[x, y]
            
            if pixel == white_color:
                tmp.append(pixel)
            else:
                tmp.append(black_color)

        out.append(tmp)
        tmp = []

    return out


def print_arr_nicely(arr, solid="X", empty="0"):
    for line in arr:
        for l in line:
            if l == (0, 0, 0, 255):
                print(empty, end=" ")
            else:
                print(solid, end=" ")

        print()


def magnify_array(arr, multiplier):
    out, tmp = [], []

    for row in arr:
        for element in row:
            tmp.extend([element for i in range(multiplier)])

        [out.append(tmp) for i in range(multiplier)]
        tmp = []
    
    return out


def reduce_array(arr, factor):
    out, tmp = [], []

    for y in range(0, len(arr), factor):
        for x in range(0, len(arr[y]), factor):
            tmp.append(arr[y][x])

        out.append(tmp)
        tmp = []
    
    return out


def character_is_at_pos(arr_total, character_array, pos, blank_color=(0, 0, 0)):
    # Checka så att den inte går utanför!

    for y, row in enumerate(character_array):
        for x, element in enumerate(row):
            if pos + x < len(arr_total[0]):
                if not arr_total[y][pos + x] == character_array[y][x]:
                    return False
            else:
                return False

    if pos + len(character_array[0]) >= len(arr_total[0]):
        return True

    for y in range(len(character_array)):
        if not arr_total[y][pos + len(character_array[0])] == blank_color:
            return False
    
    return True


# Ta bort alla eventuella spaces i slutet!
def read_characters(img, factor=10):
    characters = get_characters()

    arr1 = convert_to_black_and_white_array(img)
    arr2 = reduce_array(arr1, factor)

    length = len(arr2[0])
    out = ""
    pos = 0

    while pos < length:
        for c in characters:
            if character_is_at_pos(arr2, c[0], pos):
                out += c[1]
                pos += c[2]
                break
        
        out += ""
        pos += 1
    

    return out


def save_array_as_image(arr, img_name):
    w, h = len(arr[0]), len(arr)
    img = Image.new(mode="RGB", size=(w, h), color=(0, 0, 0))

    for y in range(h):
        for x in range(w):
            img.putpixel((x, y), arr[y][x])
        
    img.save(img_name)


def concatenate_arrays(arr1, arr2):
    if arr1 == []:
        return arr2

    out, tmp = [], []

    for row1, row2 in zip(arr1, arr2):
        tmp = row1
        tmp.extend(row2)
        out.append(tmp)
    
    return list(tuple(out))


def text_to_arrays(text, characters):
    out = []
    spacing = [[(0, 0, 0)], [(0, 0, 0)], [(0, 0, 0)], [(0, 0, 0)], [(0, 0, 0)], [(0, 0, 0)], [(0, 0, 0)]]
    c = 0

    for i, character in enumerate(text):
        for q in characters:
            if q[1] == character:
                c = q
                break

        out = concatenate_arrays(out, c[0])

        if not i == len(text) - 1:
            out = concatenate_arrays(out, spacing)
    
    return out


def text_to_image(text, name, factor=10):
    characters = get_characters()

    arr = text_to_arrays(text, characters)

    arr2 = magnify_array(arr, factor)

    save_array_as_image(arr2, name)


def get_coordinates(gui=3, margin=23):
    universal = (26 * gui, 92 * gui + margin, 219 * gui, 7 * gui)

    ag.screenshot("images_program/coordinates.png", region=universal)

    raw_coords = read_characters("images_program/coordinates.png", factor=gui)

    if raw_coords[-1] == " ":

        i = 0
        while raw_coords[-(i + 1)] == " ":
            i += 1

        raw_coords = raw_coords[:-i]

    raw_coords = raw_coords.split(" / ")


    coords = tuple(map(lambda x: float(x), raw_coords))
    return coords


def get_direction(gui=3, margin=23):
    universal = (100 * gui, 119 * gui + margin, 161 * gui, 7 * gui)

    ag.screenshot("images_program/direction.png", region=universal)

    raw_coords = read_characters("images_program/direction.png", factor=gui)

    i = 0
    while raw_coords[i] != "(":
        i += 1
    
    i += 1
    raw_coords = raw_coords[i:]
    i = 0
    while raw_coords[i] != " ":
        i += 1
    
    dir1 = raw_coords[:i]
    i += 3
    j = 0

    while raw_coords[i + j] != ")":
        j += 1

    dir2 = raw_coords[i:i + j]
    coords = (float(dir1), float(dir2))

    return coords


def main():
    
    # characters = get_characters()

    # for c in characters:
    #     print_arr_nicely(c[0], empty=" ")
    #     print()

    # arr = convert_to_black_and_white_array(NUMBER_7)

    # arr2 = magnify_array(arr, 8)

    # arr3 = reduce_array(arr2, 4)

    # print_arr_nicely(arr3, empty=" ")


    # arr = convert_to_black_and_white_array(NUMBER_9)
    # arr2 = magnify_array(arr, 100)
    # save_array_as_image(arr2, "new_9.png")


    # arr1 = convert_to_black_and_white_array(NUMBER_7)
    # arr2 = convert_to_black_and_white_array(NUMBER_9)
    # arr3 = concatenate_arrays(arr1, arr2)
    # arr4 = magnify_array(arr3, 100)
    # save_array_as_image(arr4, "new_79.png")


    #text_to_image("123 987", 10, "new_123.png", characters)

    # arr = convert_to_black_and_white_array(NUMBER_7)
    # arr2 = magnify_array(arr, 4)




    # text_to_image("123 4/5/6 (789)", "test.png", factor=10)
    # tmp = read_characters("test.png", factor=10)
    # print(tmp)


    #time.sleep(5)
    #ag.screenshot("coordinates.png", region=windows_coordinates_1920_1080_GUI3)


    # (78, 299, 621, 21)

    #m23 k92

    # 3: 299
    # 4: 391

    #with_gui = (universal[0] * gui, universal[1], universal[2] * gui, universal[3] * gui)

    #windows_coordinates_1920_1080_GUI3 = ((78*4) / 3, 250, (621 * 4) / 3, 210)


    gui = 3
    margin = 23

    time.sleep(5)

    coordinates = get_coordinates(gui=gui, margin=margin)
    direction = get_direction(gui=gui, margin=margin)

    print(coordinates)
    print(direction)




if __name__ == "__main__":
    main()