# Credit to https://www.minecraftforum.net/forums/minecraft-java-edition/redstone-discussion-and/commands-command-blocks-and/2980388-1-14-1-17-multiple-commands-in-one-command-block

def compress_command(commands):

    start = "summon falling_block ~ ~.5 ~ {Time:1,BlockState:{Name:redstone_block},Passengers:[{id:armor_stand,Health:0,Passengers:[{id:falling_block,Time:1,BlockState:{Name:activator_rail},Passengers:[{id:command_block_minecart,Command:'gamerule commandBlockOutput false'},"
    middle_start = "{id:command_block_minecart,Command:'"
    middle_end = "'},"
    end = "{id:command_block_minecart,Command:'setblock ~ ~1 ~ command_block{auto:1,Command:" + '"fill ~ ~ ~ ~ ~-3 ~ air"' + "}'},{id:command_block_minecart,Command:'kill @e[type=command_block_minecart,distance=..1]'}]}]}]}"

    total = start

    for cmd in commands:
        total += middle_start + cmd + middle_end
    
    total += end

    return total


def main():
    commands = ["say " + str(x) for x in range(1, 1000)]
    c = compress_command(commands)
    print(c)


if __name__ == "__main__":
    main()