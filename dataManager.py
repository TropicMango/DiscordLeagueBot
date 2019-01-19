import math
from pathlib import Path


def pick_champ(player, champ):
    with open("./data/{}.txt".format(player), "w") as f:
        f.write('g:0\n')  # gold
        f.write('ID:2\n')  # selected champ | skin
        f.write(champ + '|1|0|100|0\n')  # champ:strength|skin


def add_champ(player, champ, skin):
    with open("./data/{}.txt".format(player), "a") as f:
        f.write(champ + '|1|0|100|{}\n'.format(skin))  # champ:strength|skin


def started(player):
    return Path('./data/{}.txt'.format(player)).is_file()


def add_gold(player, cs, members):
    amount = cs * members
    with open("./data/{}.txt".format(player), "r") as f:
        content = f.readlines()
    leveled_up = False
    split_champ = content[int(content[1][3:])].split('|')
    current_exp = int(split_champ[2]) + amount
    current_lv = int(split_champ[1])
    while current_exp > math.pow(current_lv, 2):
        current_exp -= math.pow(current_lv, 2)
        current_lv += 1
        split_champ[3] = int(split_champ[3]) + 5
        leveled_up = True
    split_champ[2] = current_exp
    split_champ[1] = current_lv
    with open("./data/{}.txt".format(player), "w") as f:
        for line in content:
            if line.startswith('g:'):
                f.write('g:{}\n'.format(int(line.split(':')[1]) + amount))
            elif line.startswith(split_champ[0]):
                f.write('|'.join(str(x) for x in split_champ))
            else:
                f.write(line)
    msg = "<@!{}> earned {} gold for {} per minion~".format(player, amount, members)
    if leveled_up:
        msg += "\n {} is now level {}" .format(split_champ[0], current_lv)
    return msg


def get_gold(player):
    with open("./data/{}.txt".format(player), "r") as f:
        content = f.readlines()
    return content[0][2:-1]


def get_champs(player):
    with open("./data/{}.txt".format(player), "r") as f:
        content = f.readlines()
    content.pop(0)
    content.pop(0)
    i = 1
    final = []
    for line in content:
        final.append("{}. {}|Strength: {}".format(i, line.split('|')[0], line.split('|')[3]))
        i += 1
    return final


def get_my_champ(player):
    with open("./data/{}.txt".format(player), "r") as f:
        content = f.readlines()
    split_champ = content[int(content[1][3:])].split('|')
    final = ['{}_{}'.format(split_champ[0], split_champ[4][:-1]),
             'Lv: {}, Strength: {} mangos'.format(split_champ[1], split_champ[3])]
    return final


def get_my_strength(player):
    with open("./data/{}.txt".format(player), "r") as f:
        content = f.readlines()
    return content[int(content[1][3:])].split('|')[3]


def change_mvp(player, mvp):
    with open("./data/{}.txt".format(player), "r") as f:
        content = f.readlines()
    new_champ = content[int(mvp) + 1].split(':')[0]
    with open("./data/{}.txt".format(player), "w") as f:
        for line in content:
            if line.startswith('ID:'):
                f.write('ID:{}\n'.format(int(mvp) + 1))
            else:
                f.write(line)
    return new_champ.split('|')[0]
