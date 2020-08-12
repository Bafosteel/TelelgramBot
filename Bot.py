import telebot
from random import randrange
from AdvCheck import item_is_available, price_change
import time
from Databases import DataBase
from Settings import token, stickers, States

bot = telebot.TeleBot(token)
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('Привет','Пока')
keyboard.row("Добавить Сайты","Удалить Сайты")
keyboard.row('Начать отслеживание')
keyboard.row('Остановить отслеживание')

keyboard1=telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('Назад',)

keyboard2=telebot.types.ReplyKeyboardMarkup(True)
keyboard2.row('Завершить',)

sites = {}
status_tracking = {}
state = {}

def get_current_state(user_id):
        try:
            return state[user_id] # Если используете Vedis версии ниже, чем 0.7.1, то .decode() НЕ НУЖЕН
        except KeyError:  # Если такого ключа почему-то не оказалось
            return States.S_START.value

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'Привет, чтобы получить список команд, напиши: /help',reply_markup=keyboard)
    state[message.chat.id] = States.S_START.value

@bot.message_handler(commands=['help'])
def get_help(message):
    c = ('/start', '/help', '/sticker', '/check', '/reset')
    bot.send_message(message.chat.id,'Список команд: \n'
                                     '' + str(c[0]) + ' - Запуск бота\n'
                                     '' + str(c[1]) + ' - Запросить список команд\n'
                                     '' + str(c[2]) + ' - Получить случайный стикер\n'
                                     '' + str(c[3]) + ' - Разовая проверка сайтов\n'
                                     '' + str(c[4]) + ' - Сброс к началу диалога\n',reply_markup=keyboard)

@bot.message_handler(commands=['reset'])
def set_reset(message):
    state[message.chat.id] = States.S_START.value
    bot.send_message(message.chat.id, 'OK', reply_markup=keyboard)

@bot.message_handler(commands=['sticker'])
def sticker(message):
    bot.send_message(message.chat.id, '{}, Отправь мне какой-нибудь стикер,'.format(message.from_user.first_name) + \
                     'а я тебе скину скину какой-нибудь другой в ответ',reply_markup=keyboard1)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBJPNfKSs1B3-xxnTTF3tr-13taL07kwACKgAD3B1fMqNoeCFD9xUFGgQ')
    state[message.chat.id] = States.S_SEND_STICKER.value

@bot.message_handler(commands=['check'])
def check_data(message):
    db = DataBase()
    s = db.select_data()
    print(s)
    if len(s) == 0:
        no_sites_available(message)
    else:
        for site in s:
            info = item_is_available(s[site])
            if "закончился" in info:
                bot.send_message(message.chat.id, str('{}, Ответ на ваш запрос:'.format(message.from_user.first_name))
                                 + str(' ' + info))
            else:
                bot.send_message(message.chat.id,
                                 str('{}, Ответ на ваш запрос:'.format(message.from_user.first_name)) +
                                 str(' Все хорошо'))



@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_SEND_STICKER.value)
@bot.message_handler(content_types='sticker')
def send_st(message):
    try:
        if message.text.lower() == 'назад':
            set_reset(message)
        else:
            bot.send_sticker(message.chat.id, stickers[randrange(1, 12)],reply_markup=keyboard1)
    except AttributeError:
        bot.send_sticker(message.chat.id, stickers[randrange(1, 12)], reply_markup=keyboard1)


@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_ENTER_LINK)
def add_links(message):
    print('das')
    try:
        if message.text.lower() == 'завершить':
            set_reset(message)
        else:
            for entity in message.entities:  # Пройдёмся по всем entities в поисках ссылок
                # url - обычная ссылка, text_link - ссылка, скрытая под текстом
                if entity.type in ["url", "text_link"]:
                    db = DataBase()
                    db.insert_data(message)
                    bot.send_message(message.chat.id, "Объект Кампания-ссылка добавлен для отслеживания",
                                     reply_markup=keyboard2)
                else:
                    bot.send_message(message.chat.id, "Кажется, ты отправил мне что-то другое", reply_markup=keyboard2)
    except (AttributeError, TypeError):
        bot.send_message(message.chat.id, "Кажется, ты отправил мне что-то другое", reply_markup=keyboard2)

@bot.message_handler(func=lambda message: message.entities is not None)
def delete_links(message):
    for entity in message.entities:  # Пройдёмся по всем entities в поисках ссылок
        # url - обычная ссылка, text_link - ссылка, скрытая под текстом
        if entity.type in ["url", "text_link"]:
            # Мы можем не проверять chat.id, он проверяется ещё в хэндлере
            bot.delete_message(message.chat.id,message.message_id)
            bot.send_message(message.chat.id,'Ты что-то не то мне отправил?')
        else:
            return

@bot.message_handler(func=lambda message: get_current_state(message.chat.id) == States.S_ENTER_CAMPAIGN_NAME)
def delete_campaigns(message):
    try:
        if message.text.lower() == 'завершить':
            set_reset(message)
        else:
            db = DataBase()
            suc = db.delete_data(message)
            bot.send_message(message.chat.id,suc,reply_markup=keyboard2)
    except (AttributeError, TypeError):
        bot.send_message(message.chat.id, "Кажется, ты отправил мне что-то другое", reply_markup=keyboard2)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id,'Здарова, {}'.format(message.from_user.first_name))
        bot.send_sticker(message.chat.id,'CAACAgIAAxkBAAEBJL1fKSNQxKEaoHIvimcOgvPGomud6gACZwADcQtCBbSvNtH6NZIvGgQ')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id,'Пока, {}'.format(message.from_user.first_name))
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBJL9fKSRgVm-X3HeIvq4vI8A9jJOCAAMgAQAC0t1pBSOWz2dcShYvGgQ')
    elif message.text.lower() == 'начать отслеживание':
        if len(DataBase().select_data()) != 0:
            status_tracking['value'] = 1
            state[message.chat.id] = States.S_START_TRACKING_CAMPAIGN
            adv_tracking(message)
        else:
            no_sites_available(message)
    elif message.text.lower() == 'остановить отслеживание':
        status_tracking['value'] = 0
        state[message.chat.id] = States.S_STOP_TRACKING_CAMPAIGN
    elif message.text.lower() == 'добавить сайты':
        bot.send_message(message.chat.id,'{}, Отправь мне ссылки для '.format(message.from_user.first_name) + \
                                         'проверки в следующем виде Название:Сайт')
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBJPNfKSs1B3-xxnTTF3tr-13taL07kwACKgAD3B1fMqNoeCFD9xUFGgQ')
        state[message.chat.id] = States.S_ENTER_LINK

    elif message.text.lower() == 'удалить сайты':
        bot.send_message(message.chat.id,'{}, Отправь мне название кампании '.format(message.from_user.first_name) + \
                                         'для удаления пары кампания-сайт')
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBJPNfKSs1B3-xxnTTF3tr-13taL07kwACKgAD3B1fMqNoeCFD9xUFGgQ')
        state[message.chat.id] = States.S_ENTER_CAMPAIGN_NAME
    else:
        bot.send_message(message.chat.id, 'Прости, я тебя не понимаю')
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBJMFfKSUEzuXlw-KDLC8ZAT-jHfMbEQACGAEAAtLdaQV3nTANMOlAPxoE')

def adv_tracking(message):
    if status_tracking['value'] != 0:
        sites = DataBase().select_data()
        for site in sites:
            print(sites[site])
            info = item_is_available(sites[site])
            price = price_change(sites[site])
            if 'закончился' in info:
                bot.send_message(message.chat.id, str(site)+" - "+ info)
            if 'изменилась' in price:
                bot.send_message(message.chat.id, price)
        time.sleep(5) #14400
        adv_tracking(message)
    else:
        return bot.send_message(message.chat.id, 'Отслеживание остановлено')

def no_sites_available(message):
    bot.send_message(message.chat.id,
                     str('{}, Не добавлены сайты, которые мне надо отслеживать!'.format(message.from_user.first_name)))
    bot.send_sticker(message.chat.id,
                     'CAACAgIAAxkBAAEBJntfKnKGPF_Kn_pt_Kd15lNodCN9bQAC5gAD_OXdAAFciI6TzU_7cRoE')


bot.polling()
