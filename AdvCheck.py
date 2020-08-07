import requests
from bs4 import BeautifulSoup

def item_is_available(url):
    header = {'User-agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:79.0)'+ \
                           ' Gecko/20100101 Firefox/79.0', # Создаем заголовок, чтобы сайты не воспринимали нас как бота
              'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-language':'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'}
    cookies = dict(cookies_are='session=4b082e00-074c-75f7-4761-4fb12bbb343b; __utma=12798129.510440631.1596800516.'
                               '1596800516.1596800516.1; __utmc=12798129;' + \
                               ' __utmz=12798129.1596800516.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|' + \
                               'utmctr=(not%20provided); __gads=ID=19506182921d16b7:T=1596800516:S=ALNI' + \
                               '_MY-XwLcuZvDvxMnb7lEx3kAG7ideQ; __qca=P0-23977826-1596800516655;' + \
                               ' _ga=GA1.2.1387315142.1596800524; _gid=GA1.2.525403005.1596800524')
    response = requests.get(url,headers=header, cookies=cookies)
    info = ''
    soup = BeautifulSoup(response.text, 'lxml')
    if 'ozon.ru' in url: # Парсим озон
        for h2 in soup.findAll('h2'):
            if "Этот товар закончился" in str(h2.text).replace("\n","").replace("    ",""):
               info = "Товар {} закончился, либо остались только некоторые варианты".format(url)
               print(info)
    elif 'beru.ru' in url: # Парсим беру
        for span in soup.findAll('span'):
            if 'в наличии на складе' in span.text.lower():
                info='ok'
        if len(info) != 0:
            info = "Товар {} закончился, либо доставка возможна только позднее".format(url)
            print(info)
    elif 'lamoda.ru' in url: # Парсим lamoda
        for div  in soup.findAll('div',attrs={'class':'vue-widget'}):
            rating = div.find('d-add-to-cart') # В тэге хранится информация о наличии товара в магазине
            if rating:
                if rating['product-is-available']:
                    print('ok')
                    info='ok'
                else:
                    info = "Товар {} закончился, либо остались только некоторые размеры".format(url)
                    print(info)
    elif 'wildberries.ru' in url: # Парсим wildberries
        for button in soup.findAll('button',attrs={'class':'c-btn-main-lg-v1 j-add-to-wait'}):
            if 'hide' not in button['class']:
                if 'в лист ожидания' in button.text.lower():
                    info = "Товар {} закончился, либо остались только некоторые экземпляры".format(url)
    elif 'apteka.ru' in url: # Парсим аптеку
        for div in soup.findAll('div', attrs={'class':'stickProductCard__notAvailable'}):
            if 'нет в наличии' in div.text.lower():
                info = "Товар {} закончился, либо остались только некоторые экземпляры".format(url)
    elif 'detmir.ru' in url: # Парсим детский мир
        for span in soup.findAll('span'):
            if 'нет в наличии' in span.text.lower():
                info = "Товар {} закончился, либо остались только некоторые экземпляры".format(url)
    else:
        pass
    return info


def price_change(): # Данная функция отслеживает изменение цены, в том числе наличие скидки
    pass

#link = 'https://www.ozon.ru/context/detail/id/153593977/'
link = 'https://www.detmir.ru/product/index/id/2684371/'
item_is_available(link)


