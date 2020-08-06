import telebot
from random import randrange
from AdvCheck import item_is_available,price_change
import time

bot = telebot.TeleBot('############################') #post your token here
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('Привет','Пока', 'Стикер')
keyboard.row('Разовая проверка', "Добавить Сайты","Удалить Сайты")
keyboard.row('Начать отслеживание')
keyboard.row('Остановить отслеживание')

stickers = {1:'CAACAgIAAxkBAAEBJMVfKSa4sXF8U5Cr6S5g9-5VBaV8jwACGQEAAtLdaQVS6DvPqWaenxoE',
            2:'CAACAgIAAxkBAAEBJMdfKSbcR4hiQgRsQ9HivZ9oK6qhzAACFwEAAtLdaQXeYl54aAbKphoE',
            3:'CAACAgIAAxkBAAEBJMlfKSb80g5D4_R1zdiBZb5fAAEVnPwAAqsFAAIjBQ0AAQUOVw5eneNPGgQ',
            4:'CAACAgIAAxkBAAEBJMtfKScO1Aybt6uG320Xq8__m_K5EwAC1wUAAiMFDQABGQ0adjCjOEsaBA',
            5:'CAACAgIAAxkBAAEBJM9fKSdNWiG4mJiiJfhoPyoOGdlIYwACEgADdVCBE26opWd1F-9VGgQ',
            6:'CAACAgIAAxkBAAEBJNFfKSdZHkaYKoMPQ1eAFkTOoC9SRgACLgAD4djSAAH6uc0pGAABXwkaBA',
            7:'CAACAgIAAxkBAAEBJNNfKSd24KT1fJVkn2zrRLkwJZMJ2QACFQADg0cqOFMI5b7VynSqGgQ',
            8:'CAACAgIAAxkBAAEBJNVfKSecyCrPQHQbosB6f-RbwzkK1wACFAADNIWFDOGRzqE72ijUGgQ',
            9:'CAACAgIAAxkBAAEBJNdfKSfONquRlqHmwwtrhzwyofI3tgACIAADFvHqEqDWa0lrY0FgGgQ',
            10:'CAACAgIAAxkBAAEBJNlfKSfdCFp9yCiCrdMxKRI9yDSlxwAC2gAD_OXdAAEiZoo4l1XxNhoE',
            11:'CAACAgIAAxkBAAEBJRhfKUUbwt4YJCPdnjy3VbuHCLjJ1gACSwAD3B1fMs8xSfx3nsMwGgQ'}

sites = {}
data = {}
status = {}
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'Привет, чтобы получить список команд, напиши: /help',reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id,'/help, да?',reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.entities is not None)
def delete_links(message):
    for entity in message.entities:  # Пройдёмся по всем entities в поисках ссылок
        # url - обычная ссылка, text_link - ссылка, скрытая под текстом
        if entity.type in ["url", "text_link"]:
            # Мы можем не проверять chat.id, он проверяется ещё в хэндлере
            bot.send_message(message.chat.id, "Объект Кампания-ссылка добавлен для отслеживания")
            sites['test'] = str(message.text)[str(message.text).find(':') + 1:]
        else:
            return

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id,'Здарова, {}'.format(message.from_user.first_name))
        bot.send_sticker(message.chat.id,'CAACAgIAAxkBAAEBJL1fKSNQxKEaoHIvimcOgvPGomud6gACZwADcQtCBbSvNtH6NZIvGgQ')

    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id,'Пока, {}'.format(message.from_user.first_name))

        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBJL9fKSRgVm-X3HeIvq4vI8A9jJOCAAMgAQAC0t1pBSOWz2dcShYvGgQ')

    elif message.text.lower() == 'стикер':
        bot.send_message(message.chat.id,'{}, Отправь мне какой-нибудь стикер,'.format(message.from_user.first_name) + \
                                         ' а я тебе скину скину какой-нибудь другой в ответ')
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBJPNfKSs1B3-xxnTTF3tr-13taL07kwACKgAD3B1fMqNoeCFD9xUFGgQ')

    elif message.text.lower() == 'разовая проверка':
        info = item_is_available('https://www.ozon.ru/context/detail/id/153593977/')
        if len(sites) == 0:
            no_sites_available(message)
        else:
            if "закончился" in info:
                bot.send_message(message.chat.id,str('{}, Ответ на ваш запрос:'.format(message.from_user.first_name))
                                 + str(' '+ info))
            else:
                bot.send_message(message.chat.id,
                                 str('{}, Ответ на ваш запрос:'.format(message.from_user.first_name)) +
                                 str(' Все хорошо'))
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEBJndfKm89iBY2PEK6fLM-3G7Ghz1CHwACoQUAAiMFDQABTrD9oNrHRh4aBA')

    elif message.text.lower() == 'начать отслеживание':
        if len(sites) != 0:
            status['value'] = 1
            adv_tracking(message)
        else:
            no_sites_available(message)
    elif message.text.lower() == 'остановить отслеживание':
        status['value'] = 0
    elif message.text.lower() == 'добавить сайты':
        bot.send_message(message.chat.id,'{}, Отправь мне ссылки для '.format(message.from_user.first_name) + \
                                         'проверки в следующем виде Название:Сайт')
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBJPNfKSs1B3-xxnTTF3tr-13taL07kwACKgAD3B1fMqNoeCFD9xUFGgQ')
    elif message.text.lower() == 'удалить сайты':
        bot.send_message(message.chat.id,'{}, Отправь мне название кампании '.format(message.from_user.first_name) + \
                                         'для удаления пары кампания-сайт')
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBJPNfKSs1B3-xxnTTF3tr-13taL07kwACKgAD3B1fMqNoeCFD9xUFGgQ')
    else:
        bot.send_message(message.chat.id, 'Прости, я тебя не понимаю')
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBJMFfKSUEzuXlw-KDLC8ZAT-jHfMbEQACGAEAAtLdaQV3nTANMOlAPxoE')


def adv_tracking(message):
    if status['value'] != 0:
        for site in sites:
            print(sites[site])
            info = item_is_available(sites[site])
            if 'закончился':
                data[sites[site]] = info
                bot.send_message(message.chat.id, str(site)+" - "+ info)
        time.sleep(5) #14400
        adv_tracking(message)
    else:
        return bot.send_message(message.chat.id, 'Отслеживание остановлено')

def no_sites_available(message):
    bot.send_message(message.chat.id,
                     str('{}, Не добавлены сайты, которые мне надо отслеживать!'.format(message.from_user.first_name)))
    bot.send_sticker(message.chat.id,
                     'CAACAgIAAxkBAAEBJntfKnKGPF_Kn_pt_Kd15lNodCN9bQAC5gAD_OXdAAFciI6TzU_7cRoE')


@bot.message_handler(content_types=['sticker'])
def send_st(message):
    bot.send_sticker(message.chat.id, stickers[randrange(1, 12)])


bot.polling()
