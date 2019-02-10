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


champList = [
    "aatr|Aatrox|5",
    "ahri|Ahri|9",
    "akal|Akali|10",
    "alis|Alistar|11",
    "amum|Amumu|9",
    "aniv|Anivia|7",
    "anni|Annie|11",
    "ashe|Ashe|10",
    "aure|AurelionSol|2",
    "azir|Azir|4",
    "bard|Bard|3",
    "blit|Blitzcrank|10",
    "bran|Brand|6",
    "brau|Braum|5",
    "cait|Caitlyn|9",
    "cami|Camille|2",
    "cass|Cassiopeia|5",
    "chog|Chogath|7",
    "cork|Corki|8",
    "dari|Darius|7",
    "dian|Diana|4",
    "drmu|DrMundo|10",
    "drav|Draven|7",
    "ekko|Ekko|5",
    "elis|Elise|5",
    "evel|Evelynn|6",
    "ezre|Ezreal|12",
    "fidd|Fiddlesticks|9",
    "fior|Fiora|6",
    "fizz|Fizz|7",
    "gali|Galio|6",
    "gang|Gangplank|9",
    "gare|Garen|9",
    "gnar|Gnar|6",
    "grag|Gragas|10",
    "grav|Graves|9",
    "heca|Hecarim|7",
    "heim|Heimerdinger|6",
    "illa|Illaoi|2",
    "irel|Irelia|6",
    "iver|Ivern|1",
    "jann|Janna|9",
    "jarv|JarvanIV|8",
    "jax|Jax|10",
    "jayc|Jayce|4",
    "jhin|Jhin|4",
    "jinx|Jinx|6",
    "kais|Kaisa|3",
    "kali|Kalista|3",
    "karm|Karma|7",
    "kart|Karthus|6",
    "kass|Kassadin|5",
    "kata|Katarina|10",
    "kayl|Kayle|9",
    "kayn|Kayn|2",
    "kenn|Kennen|7",
    "khaz|Khazix|5",
    "kind|Kindred|2",
    "kled|Kled|2",
    "kogm|KogMaw|10",
    "lebl|Leblanc|6",
    "lees|LeeSin|9",
    "leon|Leona|8",
    "liss|Lissandra|4",
    "luci|Lucian|5",
    "lulu|Lulu|8",
    "lux|Lux|9",
    "malp|Malphite|8",
    "malz|Malzahar|7",
    "maok|Maokai|7",
    "mast|MasterYi|9",
    "miss|MissFortune|12",
    "mord|Mordekaiser|5",
    "morg|Morgana|8",
    "nami|Nami|6",
    "nasu|Nasus|8",
    "naut|Nautilus|5",
    "neek|Neeko|1",
    "nida|Nidalee|9",
    "noct|Nocturne|6",
    "nunu|Nunu|7",
    "olaf|Olaf|7",
    "oria|Orianna|8",
    "ornn|Ornn|1",
    "pant|Pantheon|8",
    "popp|Poppy|9",
    "pyke|Pyke|2",
    "quin|Quinn|4",
    "raka|Rakan|3",
    "ramm|Rammus|8",
    "reks|RekSai|2",
    "rene|Renekton|10",
    "reng|Rengar|4",
    "rive|Riven|9",
    "rumb|Rumble|4",
    "ryze|Ryze|10",
    "seju|Sejuani|7",
    "shac|Shaco|7",
    "shen|Shen|7",
    "shyv|Shyvana|6",
    "sing|Singed|9",
    "sion|Sion|5",
    "sivi|Sivir|11",
    "skar|Skarner|4",
    "sona|Sona|8",
    "sora|Soraka|9",
    "swai|Swain|4",
    "syla|Sylas|1",
    "synd|Syndra|6",
    "tahm|TahmKench|2",
    "tali|Taliyah|2",
    "talo|Talon|6",
    "tari|Taric|4",
    "teem|Teemo|10",
    "thre|Thresh|6",
    "tris|Tristana|9",
    "trun|Trundle|5",
    "tryn|Tryndamere|9",
    "twis|TwistedFate|11",
    "twit|Twitch|9",
    "udyr|Udyr|4",
    "urgo|Urgot|4",
    "varu|Varus|7",
    "vayn|Vayne|8",
    "veig|Veigar|9",
    "velk|Velkoz|3",
    "vi|Vi|6",
    "vikt|Viktor|4",
    "vlad|Vladimir|8",
    "voli|Volibear|5",
    "warw|Warwick|10",
    "wuko|Wukong|5",
    "xaya|Xayah|3",
    "xera|Xerath|4",
    "xinz|XinZhao|8",
    "yasu|Yasuo|5",
    "yori|Yorick|3",
    "zac|Zac|3",
    "zed|Zed|5",
    "zigg|Ziggs|7",
    "zile|Zilean|5",
    "zoe|Zoe|2",
    "zyra|Zyra|4",
    # champions released after 1/17 not included
]


def includes(select):
    select = ''.join(list(filter(str.isalnum, select)))
    select = select.lower()[:4]
    for name in champList:
        if name.startswith(select):
            return name.split('|')[1]
    return False


def generate():
    return champList[random.randrange(0, len(champList))].split('|')[1]


def get_skins(current_champ):
    select = current_champ.lower()[:4]
    for name in champList:
        if name.startswith(select):
            print(int(name.split('|')[2]))
            return int(name.split('|')[2])
    raise NameError


# ---------------------------- Quote Game ----------------------


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
