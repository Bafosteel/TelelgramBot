import requests
from bs4 import BeautifulSoup

class MasterClass(object):
    def __init__(self):
        self.header = {'User-agent':'#####################', # Создаем заголовок, чтобы сайты не воспринимали нас как бота
              'Accept':'######################',
              'Accept-language':'#########################'}
        self.cookies = dict(cookies_are='###################')
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