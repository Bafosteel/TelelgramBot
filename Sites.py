import requests
from bs4 import BeautifulSoup
from json import loads, decoder
from Settings import header, cookies, soup_type

class MasterClass(object):
    def __init__(self):
        self.header = header
        self.cookies = cookies
        self.soup_type = soup_type
        self.info = ''
        self.price = ''

    def extract_data(self, links):
        return self.info

    def price_changes(self, links):
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

    def price_changes(self, url):
        soup = self.parse_link(url)
        for script in soup.findAll('script',attrs={'type':'application/json',}):
            try:
                old = loads(script.string)['cellTrackingInfo']['product']['price']
                new = loads(script.string)['cellTrackingInfo']['product']['finalPrice']
                if old == new:
                    print(loads(script.string)['cellTrackingInfo']['product']['price'])
                    print(loads(script.string)['cellTrackingInfo']['product']['finalPrice'])
                    self.price = 'Цена на товар {} составляет {} руб'.format(url, old)
                    print(self.price)
                else:
                    self.price = 'Цена на товар {} изменилась с {} на {}'.format(url, old, new)
                    print(self.price)
            except KeyError as exp:
                print('Error was occurred: ' + str(exp.args[0]))
        return self.price

class BeruSite(MasterClass):

    def extract_data(self, url):
        soup = self.parse_link(url)
        for span in soup.findAll('span'):
            if 'в наличии на складе' in span.text.lower():
                self.info='ok'
        if len(self.info) != 0:
            self.info = "Товар {} закончился, либо доставка возможна только позднее".format(url)
        return self.info

    def price_changes(self, url):
        soup = self.parse_link(url)
        for script in soup.findAll('script',attrs={'type':'application/json'}):
            if "@marketplace/Fink" in script.string:
                try:
                    fin = loads(script.string)['widgets']['@marketplace/Fink'] \
                        ['/content/SkuContent/metrika']['zoneData']['price']
                    old = loads(script.string)['widgets']['@marketplace/Fink'] \
                        ['/content/SkuContent/metrika']['zoneData']['oldPrice']
                    print(loads(script.string)['widgets']['@marketplace/Fink']
                          ['/content/SkuContent/metrika']['zoneData']['oldPrice'])
                    self.price = 'Цена на товар {} изменилась с {} на {}'.format(url, old, fin)
                except KeyError:
                    print(loads(script.string)['widgets']['@marketplace/Fink']
                          ['/content/SkuContent/metrika']['zoneData']['price'])
                    cur = loads(script.string)['widgets']['@marketplace/Fink'] \
                    ['/content/SkuContent/metrika']['zoneData']['price']
                    self.price = 'Цена на товар {} составляет {} руб'.format(url,cur)
        return self.price

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

    def price_changes(self, url):
        soup = self.parse_link(url)
        for script in soup.findAll('x-product-prices',attrs={'itemprop':'offers'}):
            print(loads(script[':detailed-price']))
            if int(loads(script[':detailed-price'])['saved']) != 0:
                old = loads(script[':detailed-price'])['details'][0]['value']
                new = loads(script[':detailed-price'])['details'][1]['value']
                self.price = 'Цена на товар {} изменилась с {} на {}'.format(url, old, new)
                print(self.price)
            else:
                cur = loads(script[':detailed-price'])['details'][0]['value']
                self.price = 'Цена на товар {} составляет {} руб'.format(url, cur)
                print(self.price)
        return self.price

class WildBerriesSite(MasterClass):

    def extract_data(self, url):
        soup = self.parse_link(url)
        for button in soup.findAll('button',attrs={'class':'c-btn-main-lg-v1 j-add-to-wait'}):
            if 'hide' not in button['class']:
                if 'в лист ожидания' in button.text.lower():
                    self.info = "Товар {} закончился, либо остались только некоторые варианты".format(url)
        return self.info

    def price_changes(self, url):
        soup = self.parse_link(url)
        for script in soup.findAll('script',attrs={'type':'text/javascript'}):
            try:
                data = loads(script.string[script.string.find('google_tag_params')+20:script.string.find(';')])
                print(data)
                if 'Discount' in data:
                    new = data['Value']
                    self.price = 'Цена на товар {} изменилась и составляет {}'.format(url, new)
                    print(self.price)
                else:
                    print(data['Value'])
                    cur = data['Value']
                    self.price = 'Цена на товар {} составляет {} руб'.format(url, cur)
                    print(self.price)
            except (AttributeError, decoder.JSONDecodeError) as exp:
                print('Error was occurred: ' + str(exp.args[0]))
        return self.price

class AptekaSite(MasterClass):

    def extract_data(self, url):
        soup = self.parse_link(url)
        for div in soup.findAll('div', attrs={'class':'stickProductCard__notAvailable'}):
            if 'нет в наличии' in div.text.lower():
                self.info = "Товар {} закончился, либо остались только некоторые экземпляры".format(url)
        return self.info

    def price_changes(self, url):
        soup = self.parse_link(url)
        for script in soup.findAll('script'):
            try:
                if 'window.__INITIAL_STATE__' in script.string:
                    data = loads(script.string[script.string.find('{'):])
                    print(list(data['product']['iteminfo'].keys())[0])
                    elem = list(data['product']['iteminfo'].keys())[0]
                    new = data['product']['products'][str(elem)]['price']
                    old = data['product']['products'][str(elem)]['noDiscPrice']
                    if old == new:
                        print(data['product']['products'][str(elem)]['price'])
                        print(data['product']['products'][str(elem)]['noDiscPrice'])
                        self.price = 'Цена на товар {} составляет {} руб'.format(url, old)
                        print(self.price)
                    else:
                        self.price = 'Цена на товар {} изменилась с {} на {}'.format(url, old, new)
                        print(self.price)
            except (TypeError, decoder.JSONDecodeError, KeyError) as exp:
                print('Error was occurred: ' + str(exp.args[0]))
        return self.price

class DetMitSite(MasterClass):

    def extract_data(self, url):
        soup = self.parse_link(url)
        for span in soup.findAll('span'):
            if 'нет в наличии' in span.text.lower():
                self.info = "Товар {} закончился, либо остались только некоторые экземпляры".format(url)
        return self.info

    def price_changes(self, url):
        soup = self.parse_link(url)
        for script in soup.findAll('script', attrs={'type':'text/template', 'id':'app-data'}):
            try:
                data = loads(script.string.replace('&quot;','"'))
                print(data['product']['data']['item']['price'])
                print(data['product']['data']['item']['old_price'])
                new = data['product']['data']['item']['price']
                old = data['product']['data']['item']['old_price']
                if new != old and old is not None:
                    self.price = 'Цена на товар {} изменилась с {} на {}'.format(url, old['price'], new['price'])
                    print(self.price)
                else:
                    self.price = 'Цена на товар {} составляет {} руб'.format(url, new['price'])
                    print(self.price)

            except (KeyError, decoder.JSONDecodeError, TypeError) as exp:
                print('Error was occurred: ' + str(exp.args[0]))
        return self.price