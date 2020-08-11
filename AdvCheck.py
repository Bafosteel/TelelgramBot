from Sites import OzonSite, BeruSite, LamodaSite, WildBerriesSite, AptekaSite, DetMitSite

def item_is_available(url):
    info = ''
    if 'ozon.ru' in url: # Парсим озон
        oz = OzonSite()
        info = oz.extract_data(url)
    elif 'beru.ru' in url: # Парсим беру
        br = BeruSite()
        info = br.extract_data(url)
    elif 'lamoda.ru' in url: # Парсим lamoda
        ld = LamodaSite()
        info = ld.extract_data(url)
    elif 'wildberries.ru' in url: # Парсим wildberries
        wb = WildBerriesSite()
        info = wb.extract_data(url)
    elif 'apteka.ru' in url: # Парсим аптеку
        ap = AptekaSite()
        info = ap.extract_data(url)
    elif 'detmir.ru' in url: # Парсим детский мир
        dt = DetMitSite()
        info = dt.extract_data(url)
    else:
        pass
    return info


def price_change(url): # Данная функция отслеживает изменение цены, в том числе наличие скидки
    price = ''
    if 'ozon' in url:
        oz = OzonSite()
        oz.price_changes(url)
    elif 'beru.ru' in url:
        br = BeruSite()
        br.price_changes(url)
    elif 'lamoda.ru' in url:
        ld = LamodaSite()
        ld.price_changes(url)
    elif 'wildberries.ru' in url:
        wld = WildBerriesSite()
        wld.price_changes(url)
    elif 'apteka.ru' in url:
        apt = AptekaSite()
        apt.price_changes(url)
    elif 'detmir.ru' in url:
        dt = AptekaSite()
        dt.price_changes(url)
    else:
        pass

    return price

link = 'https://www.ozon.ru/context/detail/id/153593977/'
#link = 'https://www.detmir.ru/product/index/id/2684371/'
#item_is_available(link)
#u = 'https://beru.ru/product/nabor-ruchek-sharikovykh-sinikh-4-sht-g-3-nk-114790002/100957275453?show-uid=159715192970007211489061177&offerid=HgAOaSIp3AqHnzD40LnLvA'

#u = 'https://www.ozon.ru/product/tufli-kotofey-177582005/'
#u = 'https://www.ozon.ru/product/smartfon-huawei-smartfon-huawei-y8p-128gb-serebristyy-176016444/'

#u='https://www.lamoda.ru/p/to172emibby1/clothes-tomtailor-shorty/'
#u = 'https://www.lamoda.ru/p/mp002xm07y07/shoes-outventure-kedy/'

#u = 'https://www.wildberries.ru/catalog/11316015/detail.aspx?targetUrl=GP'
#u = 'https://www.wildberries.ru/catalog/11731387/detail.aspx?targetUrl=MI'

#u = 'https://apteka.ru/product/kasha-7-zlakov-s-yagodami-na-kozem-moloke-2000-5e4256f0aaa70200013c9503/'
#u = 'https://apteka.ru/product/zhavelon-n300-tabl-5e3274d541134b00010610a6'

#u = 'https://www.detmir.ru/product/index/id/1814601/'
u = 'https://www.detmir.ru/product/index/id/3148103/'
price_change(u)

