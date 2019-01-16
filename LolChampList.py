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
