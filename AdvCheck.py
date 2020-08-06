import requests
from bs4 import BeautifulSoup

def item_is_available(url):
    response = requests.get(url)
    info = ''
    soup = BeautifulSoup(response.text, 'lxml')
    if 'ozon.ru' in url:
        for h2 in soup.findAll('h2'):
            if "Этот товар закончился" in str(h2.text).replace("\n","").replace("    ",""):
               info = "Товар {} закончился, либо остались только некоторые размеры".format(url)
               print(info)
    elif 'beru.ru' in url:
        pass
    elif 'lamoda.ru' in url:
        pass
    elif 'wildberries.ru' in url:
        pass
    elif 'apteka.ru' in url:
        pass
    elif 'detmir.ru' in url:
        pass
    else:
        pass
    return info


def price_change():
    pass

#link = 'https://www.ozon.ru/context/detail/id/153593977/'
#item_is_available(link)
