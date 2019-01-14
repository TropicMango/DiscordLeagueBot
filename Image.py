import requests
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/59.0.3071.115 Safari/537.36 '

headers = {
    'User-Agent': USER_AGENT
}


def search_cat():
    url = 'http://thecatapi.com/api/images/get?format=xml&results_per_page=1'

    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')

    # print(resp.text)
    dict_mod = soup.find('image')
    url = dict_mod.find('url').text
    return url


# print(lookup_word('cat'))
