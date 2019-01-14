import requests
import random
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/59.0.3071.115 Safari/537.36 '

headers = {
    'User-Agent': USER_AGENT
}


def search_things(keyword):
    keyword = keyword.replace(" ", "+")
    print(keyword)

    url = 'https://images.search.yahoo.com/search/images?p={}'.format(keyword)

    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')

    pic = soup.select('img[alt=""]')
    num = (random.randrange(0, len(pic)-1))
    print(num)

    hidden = str(pic[num])

    for part in hidden.split('"'):
        if part.startswith("https://"):
            return part

    return 0



