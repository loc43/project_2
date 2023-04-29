import telebot
import random 
import time
from telebot import types

bot = telebot.TeleBot('5897065775:AAH5fCk2tIAwQD1LBDNyCZcpSfKrlSYZCqk')

task = dict()
task['Как сделать бомбочку из спичек \n Умом россию не понять'] = ['Джузеппе Верди травиата \n Скачать', 'Про размножение синичек \n Толстой Война и мир читать']
task['в стеклянных банках из под ягод \n храню всю собранную грусть'] = ['я ею счастье разбавляю \n хрусть хрусть', 'их уже больше чем варенья \n и пусть']
task['я свой характер закаляю \n преодолением преград'] = ['упорно циркулем рисую \n квадрат ', 'иду за чипсами сквозь бурю \n и град']
task['Сон меня сегодня не разнежил, \n Я проснулась рано поутру'] = ['И пошла, вдыхая воздух свежий, \n Посмотреть ручного кенгуру' , 'Услыхав незнакомцев в прихожей, \n потянулась рукой к топору']
task['я целый час молил злодеев \n не добавляйте курагу'] = ['но кто же слушает советы \n рагу' , 'но усмехались людоеды \n ну ну']
task['весной по плану гусь взгогочет \n и расщебечется щегол'] = ['а вот у выхухоли сложный \n глагол' , 'лишь я пашу зимой и летом \n как вол']
task['Когда умру, то не кладите, \n Не покупайтте мне венок.'] =['А лучше нолик положите \n На мой печальный бугорок.' , 'Пусть классный мой руководитель \n На десять лет получит строк.']
task['Как-то спокойно я вышел из ада, \n ужас распада легко перенес.'] = ['Только теперь заболело, как надо. \n Так я и думал. Отходит наркоз.' , 'Тело забрали для трепанаций. Руки по моргам. \n А где же мой нос?']


curr_ans = []
name_list = []
id_list = []
player_dict = dict()
user_list = []
right_ans = ''
names_dict = dict()
ans_counter = 0

players = []

chat_id = 0

crunches = True

class Player():
    name = ''
    score = 0
    id = 0

machine = Player()
machine.name = 'Bot'
machine.id = 0

web = False

truth = Player()
truth.name = 'Truth'
truth.id = 1

ans_dict = dict()

ref_list= []
poets_dict = dict()
poets_dict['Пастернак'] = 'https://rustih.ru/boris-pasternak/'
poets_dict['Ахматова'] = 'https://rustih.ru/anna-axmatova/'
poets_dict['Асадов'] = 'https://rustih.ru/eduard-asadov/'
poets_dict['Цветаева'] = 'https://rustih.ru/marina-cvetaeva/'
poets_dict['Бродский'] = 'https://rustih.ru/iosif-brodskij/'

poem_marker =  '<div class="entry-title"><a href='