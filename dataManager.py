def pick_champ(player, champ):
    with open("playerData.txt", "a") as f:
        f.write(player + '~0' + '|' + '0\n')
        # name~selectedID|gold
        f.write(player + '|' + champ + '~100|0\n')
        # name|champ~strength|skin~skin~skin


def started(player):
    with open("playerData.txt", "r") as f:
        line = f.readline()
        while line:
            if line.strip().startswith(player):
                return True
            line = f.readline()
    return False


def add_gold(player, amount):
    return
    with open("playerData.txt", "r") as f:
        content = f.readlines()
    # for x in range(len(content)):
    #     line = content[x]
    #     if line.startswith(player + '~'):
    #         splice_line = line.split('|')
    #         splice_line[1] = int(splice_line[1]) + amount
    #         content[x] = '|'.join(splice_line)
    #         print(content[x])
    #     break
    print('read')
    with open("playerData.txt", "w") as f:
        for line in content:
            print(line + '------------')
            if line.startswith(player + '~'):
                print('found')
                print(line)
                splice_line = line.split('|')
                splice_line[1] = int(splice_line[1]) + amount
                splice_line = '|'.join(splice_line)
                print(splice_line)
                f.write(splice_line + '\n')
            else:
                f.write(line + '\n')
