import requests
from bs4 import BeautifulSoup

def item_is_available(url):
    header = {'User-agent':'##################', # Создаем заголовок, чтобы сайты не воспринимали нас как бота
              'Accept':'####################################',
              'Accept-language':'########################'}
    cookies = dict(cookies_are='#######################')
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


