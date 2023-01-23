from PIL import Image
import block_reader
import map_program


# FIXA DENNA

def lookup_block_id(name):
    return "minecraft:" + name.lower().replace(" ", "_")

def wrapper_command_map(start_block, diff):
    def command_map(entry):
        if start_block is None:
            return "setblock" + " ~" + str(entry[1][0]) + " ~" + str(entry[1][1] + diff) + " ~" + str(entry[1][2]) + " " + lookup_block_id(entry[0])
        else:
            return "setblock " + str(entry[1][0] + start_block[0]) + " " + str(entry[1][1] + start_block[1] + diff) + " " + str(entry[1][2] + start_block[2]) + " " + lookup_block_id(entry[0])

    return command_map

def commands_from_image(file_name, blocks_palette, start_block, block_width, block_height, centralize=False, height_start=100, print_difference=False):

    img = Image.open(file_name)
    pixels = img.load()
    block_colors = block_reader.read_blocks(blocks_palette)

    dict_0_expensive = map_program.change_colors_by_id(block_colors, 0)
    dict_1_expensive = map_program.change_colors_by_id(block_colors, 1) # Tror detta är den vanliga
    dict_2_expensive = map_program.change_colors_by_id(block_colors, 2) # 255:an
    #dict_3_expensive = map_program.change_colors_by_id(block_colors, 3) # Går endast med verktyg

    all_dicts_expensive = dict_0_expensive | dict_1_expensive
    all_dicts_expensive = all_dicts_expensive | dict_2_expensive

    blocks = []
    tmp = []
    blocks_stream = []

    y_lowest = 0
    y_highest = 0

    for y in range(block_height):
        for x in range(block_width):
            block_x = x
            block_z = y
            entry = all_dicts_expensive[pixels[x, y]]

            possible_blocks = entry[0]
            id = entry[1]
            
            if id == 0:
                if y == 0:
                    block_y = -1
                else:
                    if centralize and blocks[y - 1][x][1][1] > 0:
                        block_y = 0
                    else:
                        block_y = blocks[y - 1][x][1][1] - 1
                #ned
            elif id == 1:
                if y == 0:
                    block_y = 0
                else:
                    block_y = blocks[y - 1][x][1][1]
                #samma
            elif id == 2:
                if y == 0:
                    block_y = 1
                else:
                    if centralize and blocks[y - 1][x][1][1] < 0:
                        block_y = 0
                    else:
                        block_y = blocks[y - 1][x][1][1] + 1
                #upp

            if block_y < y_lowest:
                y_lowest = block_y

            elif block_y > y_highest:
                y_highest = block_y

            tmp.append((possible_blocks[0], (block_x, block_y, block_z)))
            blocks_stream.append((possible_blocks[0], (block_x, block_y, block_z)))

        blocks.append(tmp)
        tmp = []

    difference = y_highest + abs(y_lowest)
    highest_block = height_start + y_highest + abs(y_lowest)

    if highest_block > 318:
        print("WARNING: Maximum build limit exceeded. Change the start-y of the map.")

    #print(blocks[0])
    # print(y_lowest)
    # print(y_highest)

    if print_difference:
        print("Difference: " + str(difference))
        print("Starts at: " + str(height_start))
        print("Highest block: " + str(highest_block))

    map_func = wrapper_command_map(start_block, abs(y_lowest))
    as_commands = list(map(map_func, blocks_stream))
    return as_commands


def bottom_and_topborder_commands(start_block, block_width, block_height, height=100, block_name="White Terracotta"):
    out = []

    if start_block is None:
        # Utdaterad: air och inte block_height med
        out.append("fill ~0 ~" + str(height) + " ~-1 " + "~" + str(block_width - 1) + " ~" + str(height) + " ~-1 " + lookup_block_id(block_name))
        out.append("fill ~0 ~" + str(height - 1) + " ~0 " + "~" + str(block_width - 1) + " ~" + str(height - 1) + " ~" + str(block_width - 1) + " " + lookup_block_id(block_name))
    
    else:
        out.append("fill " + str(start_block[0]) + " " + str(height) + " " + str(start_block[2] - 1) + " " + str(start_block[0] + block_width - 1) + " " + str(height) + " " + str(start_block[2] - 1) + " " + lookup_block_id("Air"))
        
        # Töm hela rummet här?
        #out.append("fill " + str(start_block[0]) + " " + str(start_block[1]) + " " + str(start_block[2]) + " " + str(start_block[0] + block_width - 1) + " " + str(start_block[1]) + " " + str(start_block[2] + block_height - 1) + " " + lookup_block_id("Air"))
        #out.append("fill " + str(start_block[0]) + " " + str(start_block[1] - 1) + " " + str(start_block[2]) + " " + str(start_block[0] + block_width - 1) + " " + str(start_block[1] - 1) + " " + str(start_block[2] + block_height - 1) + " " + lookup_block_id("Air"))

        out.append("fill " + str(start_block[0]) + " " + str(height) + " " + str(start_block[2] - 1) + " " + str(start_block[0] + block_width - 1) + " " + str(height) + " " + str(start_block[2] - 1) + " " + lookup_block_id(block_name))
        #out.append("fill " + str(start_block[0]) + " " + str(start_block[1] - 1) + " " + str(start_block[2]) + " " + str(start_block[0] + block_width - 1) + " " + str(start_block[1] - 1) + " " + str(start_block[2] + block_height - 1) + " " + lookup_block_id(block_name))

    return out


# If start_block is None, its uses ~
# Height is only used if start_block is None

def create_file(image_name, block_palette, command_file_name, start_block, map_width=1, map_height=1, centralize=False, height=100, border_block="White Terracotta", print_difference=False, remove_blocks=False):
    
    block_width, block_height = map_width * 128, map_height * 128

    commands = []

    # Speciell för 2x2?
    if remove_blocks:
        for w in range(map_width):
            for h in range(map_height):
                for i in range(height, 320): # 320 är build limit
                    commands.append("fill " + str(start_block[0] + int(w * 128 + h * 128)) + " " + str(i) + " " + str(start_block[2] + int(w * 128 + h * 128)) + " " + str(start_block[0] + int(block_width / 2) - 1 + int(w * 128 + h * 128)) + " " + str(i) + " " + str(start_block[2] + block_height - 1 + int(w * 128 + h * 128)) + " " + lookup_block_id("Air"))
                    commands.append("fill " + str(start_block[0] + int(block_width / 2) - 1 + int(w * 128 + h * 128)) + " " + str(i) + " " + str(start_block[2] + int(w * 128 + h * 128)) + " " + str(start_block[0] + block_width - 1 + int(w * 128 + h * 128)) + " " + str(i) + " " + str(start_block[2] + block_height - 1 + int(w * 128 + h * 128)) + " " + lookup_block_id("Air"))

    commands.extend(bottom_and_topborder_commands(start_block, block_width, block_height, height=height, block_name=border_block))
    commands.extend(commands_from_image(image_name, block_palette, start_block, block_width, block_height, centralize=centralize, height_start=height, print_difference=print_difference))

    with open(command_file_name, "w") as f:
        for command in commands:
            f.write(command + "\n")


def main():

    start_block = (1000, 1000, 1000)

    create_file("images/final.png", "palettes/blocks_palette_all.txt", "commands.txt", start_block)



    # Fixa rätt blocknamn
    # Commandmaskin, eller gör program som skriver?

    # Kolla så att färgerna stämmer
    # Prova om det går att sätta ut kelp
    # Gör egen palette från fil
    # Banna block från fil? Eller kanske bara göra att man tar bort en färg från alla block
    # Gör interface för att välja palette och bildnamn

    # Avstånd mellan högsta och lägsta
    # Öka allt med lägsta blockets höjd
    # Optimera antalet block som sätts ut

    # När flera maps, gör en i taget?
    # Oavsett: fixa bakgrund och air (måste vara färre än 32 000 block)

    # Lägg till datapack?

    # /gamerule maxCommandChainLength behöver ändras?
    # //gamerule maxCommandChainLength 2147483647


if __name__ == "__main__":
    main()