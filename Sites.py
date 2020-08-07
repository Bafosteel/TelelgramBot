import requests
from bs4 import BeautifulSoup

class MasterClass(object):
    def __init__(self):
        self.header = {'User-agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:79.0)'+ \
                           ' Gecko/20100101 Firefox/79.0', # Создаем заголовок, чтобы сайты не воспринимали нас как бота
              'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
              'Accept-language':'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'}
        self.cookies = dict(cookies_are='session=4b082e00-074c-75f7-4761-4fb12bbb343b; __utma=12798129.510440631.1596800516.'
                               '1596800516.1596800516.1; __utmc=12798129;' + \
                               ' __utmz=12798129.1596800516.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|' + \
                               'utmctr=(not%20provided); __gads=ID=19506182921d16b7:T=1596800516:S=ALNI' + \
                               '_MY-XwLcuZvDvxMnb7lEx3kAG7ideQ; __qca=P0-23977826-1596800516655;' + \
                               ' _ga=GA1.2.1387315142.1596800524; _gid=GA1.2.525403005.1596800524')
        self.soup_type='lxml'
        self.info = ''
        self.price = ''

    def extract_data(self, links):
        return self.info

    def price_changes(self):
        return self.price

    def parse_link(self, url):
        response = requests.get(url, headers=self.header, cookies=self.cookies)
        soup = BeautifulSoup(response.text, str(self.soup_type))
        return soup


class OzonSite(MasterClass):

    def extract_data(self, url):
        soup = self.parse_link(url)
        for h2 in soup.findAll('h2'):
            if "Этот товар закончился" in str(h2.text).replace("\n", "").replace("    ", ""):
                self.info = "Товар {} закончился, либо остались только некоторые размеры".format(url)
        return self.info

    def price_changes(self):
        pass

class BeruSite(MasterClass):

    def extract_data(self, url):
        soup = self.parse_link(url)
        for span in soup.findAll('span'):
            if 'в наличии на складе' in span.text.lower():
                self.info='ok'
        if len(self.info) != 0:
            self.info = "Товар {} закончился, либо доставка возможна только позднее".format(url)
        return self.info

    def price_changes(self):
        pass

class LamodaSite(MasterClass):

    def extract_data(self, url):
        soup = self.parse_link(url)
        for div  in soup.findAll('div',attrs={'class':'vue-widget'}):
            rating = div.find('d-add-to-cart') # В тэге хранится информация о наличии товара в магазине
            if rating:
                if rating['product-is-available']:
                    self.info='ok'
                else:
                    self.info = "Товар {} закончился, либо остались только некоторые размеры".format(url)
        return self.info

    def price_changes(self):
        pass

class WildBerriesSite(MasterClass):

    def extract_data(self, url):
        soup = self.parse_link(url)
        for button in soup.findAll('button',attrs={'class':'c-btn-main-lg-v1 j-add-to-wait'}):
            if 'hide' not in button['class']:
                if 'в лист ожидания' in button.text.lower():
                    self.info = "Товар {} закончился, либо остались только некоторые варианты".format(url)
        return self.info

    def price_changes(self):
        pass

class AptekaSite(MasterClass):

    def extract_data(self, url):
        soup = self.parse_link(url)
        for div in soup.findAll('div', attrs={'class':'stickProductCard__notAvailable'}):
            if 'нет в наличии' in div.text.lower():
                self.info = "Товар {} закончился, либо остались только некоторые экземпляры".format(url)
        return self.info

    def price_changes(self):
        pass

class DetMitSite(MasterClass):

    def extract_data(self, url):
        soup = self.parse_link(url)
        for span in soup.findAll('span'):
            if 'нет в наличии' in span.text.lower():
                self.info = "Товар {} закончился, либо остались только некоторые экземпляры".format(url)
        return self.info

    def price_changes(self):
        pass