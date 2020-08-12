from enum import Enum

class States(Enum):
    """
    Мы используем словарь, в которой храним всегда строковые данные,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_ENTER_LINK = "1"
    S_ENTER_CAMPAIGN_NAME = "2"
    S_START_TRACKING_CAMPAIGN = "3"
    S_STOP_TRACKING_CAMPAIGN = "4"
    S_SEND_STICKER = "5"

token = '***********************'
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

header = {'User-agent':'**********************', # Создаем заголовок, чтобы сайты не воспринимали нас как бота
              'Accept':'*****************************',
              'Accept-language':'****************************'}
cookies = dict(cookies_are='*********************')
soup_type = 'lxml'
auth = {'user':'**********', 'password':'*************************'}
