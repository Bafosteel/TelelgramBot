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
        price = oz.price_changes(url)
    elif 'beru.ru' in url:
        br = BeruSite()
        price = br.price_changes(url)
    elif 'lamoda.ru' in url:
        ld = LamodaSite()
        price = ld.price_changes(url)
    elif 'wildberries.ru' in url:
        wld = WildBerriesSite()
        price = wld.price_changes(url)
    elif 'apteka.ru' in url:
        apt = AptekaSite()
        price = apt.price_changes(url)
    elif 'detmir.ru' in url:
        dt = AptekaSite()
        price = dt.price_changes(url)
    else:
        pass

    return price
