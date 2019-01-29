import requests
import math
from bs4 import BeautifulSoup
import random

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

headers = {
    'User-Agent': USER_AGENT
}
champ = ""
attempt = 0


def gen_champ():
    champ_list = {
        0: "Aatrox",
        1: "Ahri",
        2: "Akali",
        3: "Alistar",
        4: "Amumu",
        5: "Anivia",
        6: "Annie",
        7: "Ashe",
        8: "Aurelion_Sol",
        9: "Azir",
        10: "Bard",
        11: "Blitzcrank",
        12: "Brand",
        13: "Braum",
        14: "Caitlyn",
        15: "Camille",
        16: "Cassiopeia",
        17: "Cho'Gath",
        18: "Corki",
        19: "Darius",
        20: "Diana",
        21: "Dr.Mundo",
        22: "Draven",
        23: "Ekko",
        24: "Elise",
        25: "Evelynn",
        26: "Ezreal",
        27: "Fiddlesticks",
        28: "Fiora",
        29: "Fizz",
        30: "Galio",
        31: "Gangplank",
        32: "Garen",
        33: "Gnar",
        34: "Gragas",
        35: "Graves",
        36: "Hecarim",
        37: "Heimerdinger",
        38: "Illaoi",
        39: "Irelia",
        40: "Ivern",
        41: "Janna",
        42: "Jarvan_IV",
        43: "Jax",
        44: "Jayce",
        45: "Jhin",
        46: "Jinx",
        47: "Kalista",
        48: "Karma",
        49: "Karthus",
        50: "Kassadin",
        51: "Katarina",
        52: "Kayle",
        53: "Kayn",
        54: "Kennen",
        55: "Kha'Zix",
        56: "Kindred",
        57: "Kled",
        58: "Kog'Maw",
        59: "LeBlanc",
        60: "Lee_Sin",
        61: "Leona",
        62: "Lissandra",
        63: "Lucian",
        64: "Lulu",
        65: "Lux",
        66: "Malphite",
        67: "Malzahar",
        68: "Maokai",
        69: "Master_Yi",
        70: "Miss_Fortune",
        71: "Mordekaiser",
        72: "Morgana",
        73: "Nami",
        74: "Nasus",
        75: "Nautilus",
        76: "Nidalee",
        77: "Nocturne",
        78: "Nunu",
        79: "Olaf",
        80: "Orianna",
        81: "Ornn",
        82: "Pantheon",
        83: "Poppy",
        84: "Quinn",
        85: "Rakan",
        86: "Rammus",
        87: "Rek'Sai",
        88: "Renekton",
        89: "Rengar",
        90: "Riven",
        91: "Rumble",
        92: "Ryze",
        93: "Sejuani",
        94: "Shaco",
        95: "Shen",
        96: "Shyvana",
        97: "Singed",
        98: "Sion",
        99: "Sivir",
        100: "Skarner",
        101: "Sona",
        102: "Soraka",
        103: "Swain",
        104: "Syndra",
        105: "Tahm_Kench",
        106: "Taliyah",
        107: "Talon",
        108: "Taric",
        109: "Teemo",
        110: "Thresh",
        111: "Tristana",
        112: "Trundle",
        113: "Tryndamere",
        114: "Twisted_Fate",
        115: "Twitch",
        116: "Udyr",
        117: "Urgot",
        118: "Varus",
        119: "Vayne",
        120: "Veigar",
        121: "Vel'Koz",
        122: "Vi",
        123: "Viktor",
        124: "Vladimir",
        125: "Volibear",
        126: "Warwick",
        127: "Wukong",
        128: "Xayah",
        129: "Xerath",
        130: "Xin_Zhao",
        131: "Yasuo",
        133: "Zac",
        132: "Yorick",
        134: "Zed",
        135: "Ziggs",
        136: "Zilean",
        137: "Zyra",
    }
    global champ
    champ = champ_list.get(random.randrange(0, 137), 5)
    global attempt
    attempt = 0
    print(champ)
    if champ == "":
        return "New Champ"
    else:
        return "Welcome to Guess the Champ"


def hint():
    if champ == "":
        return "The Game has not Started yet!"
    url = 'http://leagueoflegends.wikia.com/wiki/{}/Quotes'.format(champ)
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')

    movement = soup.find_all("ul")

    lines = []
    for x in range(19, len(movement)-13):
        # print("------------------------------------------------------------"+str(x))
        for line in movement[x].find_all("i"):
            # print(line.text)
            lines.append(line.text)

    quote = lines[random.randrange(0, len(lines) - 1)]
    while champ in quote:
        quote = lines[random.randrange(0, len(lines) - 1)]
    global attempt
    attempt += 1
    # print(attempt)
    return quote


def answer(name):
    if answer_mod(name.lower()) == champ.lower():
        score = 50/math.pow(attempt+1, 2)
        gen_champ()
        return "That is correct! You earned {} points".format(str(round(score, 2))+"\n new champ generated")
    elif name == "":
        temp = champ
        gen_champ()
        return "the answer was {}".format(temp)
    else:
        return "That's not the right answer"


def answer_mod(name):
    if name.find(" ") == -1:
        return name
    name.replace(" ", "_")
    return name


if __name__ == "__main__":
    gen_champ()
    print(hint())
    print(hint())
    print(hint())
