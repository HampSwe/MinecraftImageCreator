import csv


def parse_blocks(str):

    blocks = []
    tmp = ""

    opened = False
    opened_block = None

    i = 0

    while i < len(str):

        if str[i] == "(":
            blocks.append(tmp[:-1])
            opened = True
            opened_block = tmp
            tmp = ""
        
        elif str[i] == ")":
            opened = False
            blocks.append(opened_block + tmp)
            tmp = ""
            i += 2

        elif str[i] != ",":
            tmp += str[i]

        else:
            if opened:
                blocks.append(opened_block + tmp)
                #i += 1
            else:
                blocks.append(tmp)

            tmp = ""
            i += 1

        if i >= len(str):
            break
            
        i += 1
    
    if not tmp == "":
        blocks.append(tmp)

    return blocks


def save_to_file(colors, blocks, name="blocks_all_produced"):
    with open("palettes/" + name + ".txt", "w") as f:
        for (a, b) in zip(colors, blocks):

            #print(a[0])
            f.write(str(a[0]) + ", " + str(a[1]) + ", " + str(a[2]) + "\n")

            for i, block in enumerate(b):
                if i != len(b) - 1:
                    f.write(str(block) + ", ")
                else:
                    f.write(str(block) + "\n")

            #f.write(b + "\n")


def read_blocks(file_name):

    final_dict = dict()

    with open(file_name) as f:
        lines = f.readlines()

        for i in range(0, len(lines), 2):
            if lines[i][-2:] == "\n":
                cst = lines[i][:-2]
            else:
                cst = lines[i][:-1]

            cs = tuple([int(x) for x in cst.split(", ")])
            #print(cs)
            blocks = lines[i + 1][:-1].split(", ")

            final_dict[cs] = blocks
    
    return final_dict





def main():

    block_colors_all = dict()

    all_colors = []
    all_possible_blocks = []

    with open("block_data/block_colors.csv") as csv_file:
        blocks = csv.reader(csv_file)

        for i, row in enumerate(blocks):

            if not i == 0:
                #print(row)

                c = tuple([int(x) for x in row[2].split(", ")])
                possible_blocks = parse_blocks(str(row[3]))

                all_colors.append(c)
                all_possible_blocks.append(possible_blocks)

                # print(c)
                # print(str(row[3]))
                # print(possible_blocks)
                # print()

        
        save_to_file(all_colors, all_possible_blocks)

    print(read_blocks("palette_all.txt"))


if __name__ == "__main__":
    main()