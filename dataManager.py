from pathlib import Path


def pick_champ(player, champ):
    with open("./data/{}.txt".format(player), "w") as f:
        f.write('g:0\n')  # gold
        f.write('ID:0\n')  # selected champ | skin
        f.write(champ + ':100|0\n')  # champ:strength|skin


def started(player):
    return Path('./data/{}.txt'.format(player)).is_file()


def add_gold(player, amount):
    with open("./data/{}.txt".format(player), "r") as f:
        content = f.readlines()
    with open("./data/{}.txt".format(player), "w") as f:
        for line in content:
            if line.startswith('g:'):
                f.write('g:{}\n'.format(int(line.split(':')[1]) + amount))
            else:
                f.write(line)


def get_gold(player):
    with open("./data/{}.txt".format(player), "r") as f:
        content = f.readlines()
    return content[0][2:-1]


def get_champs(player):
    with open("./data/{}.txt".format(player), "r") as f:
        content = f.readlines()
    content.pop(0)
    content.pop(0)
    i = 0
    final = []
    for line in content:
        final.append(line.split(':')[0] + "|ID: {}, Strength: {}".format(i, line.split(':')[1].split('|')[0]))
        i += 1
    return final


def get_my_champ(player):
    with open("./data/{}.txt".format(player), "r") as f:
        content = f.readlines()
    selected_champ = int(content[1][3:]) + 2
    split_champ = content[selected_champ].split(':')
    final = ['{}_{}'.format(split_champ[0], split_champ[1].split('|')[1][:-1]),
             'Strength: {} mangos'.format(split_champ[1].split('|')[0])]
    return final


def change_mvp(player, ide):
    with open("./data/{}.txt".format(player), "r") as f:
        content = f.readlines()
    new_champ = content[int(ide) + 2].split(':')[0]
    with open("./data/{}.txt".format(player), "w") as f:
        for line in content:
            if line.startswith('ID:'):
                f.write('ID:{}\n'.format(ide))
            else:
                f.write(line)
    return new_champ
