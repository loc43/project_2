import random
import requests
from globals import bot, curr_ans, player, player_list
import globals
from telebot import types
#игра для чата, с интернетом

ref_list= []
poets_dict = dict()
poets_dict['Пастернак'] = 'https://rustih.ru/boris-pasternak/'
poets_dict['Ахматова'] = 'https://rustih.ru/anna-axmatova/'
poets_dict['Асадов'] = 'https://rustih.ru/eduard-asadov/'
poets_dict['Цветаева'] = 'https://rustih.ru/marina-cvetaeva/'
poets_dict['Бродский'] = 'https://rustih.ru/iosif-brodskij/'

poem_marker =  '<div class="entry-title"><a href='

def find_poem(url):
    response = requests.get(url)
    decoded = response.text
    tmp = decoded
    while poem_marker in tmp:
        idx = tmp.index(poem_marker)
        a = ''
        for elem in tmp[idx + len(poem_marker) + 1 : ]:
            if elem == '"':
                break
            a += elem
        ref_list.append(a)
        tmp = tmp[idx + 10 : ]
    return random.choice(ref_list)


def find_end(str):
    cnt = 0
    sum = 0
    tmp = str
    while cnt < 4:
        idx = tmp.index('>')
        tmp = tmp[idx + 1 : ]
        cnt += 1
        sum += idx + 1
    return sum

def find_text(url):
    response = requests.get(url)
    decoded = response.text
    start_marker = '<div class="entry-content poem-text" itemscope itemtype="http://schema.org/CreativeWork">'
    idx_1 = decoded[ : 50000].index(start_marker)
    tmp = decoded[idx_1 + len(start_marker) + 6: idx_1 + 500]
    try:
        idx_2 = tmp.index('<p>')
    except:
        idx_2 = find_end(tmp)
    return(decipher(tmp[ : idx_2]))


def decipher(list):
    while '<' in list:
        list = list[ : list.index('<')] + list[list.index('>') + 1 : ]
    while '&#8212;' in list:
        list = list[ : list.index('&#8212;')] + '--' + list[list.index('&#8212;') + 7:] 
    while '&#8230;' in list:
        list = list[ : list.index('&#8230;')] + '!' + list[list.index('&#8230;') + 7:] 
    while '&#171;' in list:
        list = list[ : list.index('&#171;')] + '"' + list[list.index('&#171;') + 6:] 
    while '&#187;' in list:
        list = list[ : list.index('&#187;')] + '"' + list[list.index('&#187;') + 6:] 
    return list

def init_web(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.register_next_step_handler(message, init_web1)
    btn1 = types.KeyboardButton('Ахматова')
    btn2 = types.KeyboardButton('Цветаева')
    btn3 = types.KeyboardButton('Пастернак')
    btn4 = types.KeyboardButton('Бродский')
    btn5 = types.KeyboardButton('Асадов')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.from_user.id, 'выбери поэта', reply_markup = markup)


def init_web1(message):
    list = find_text(find_poem(poets_dict[message.text]))
    try:
        idx_1 = list.index('\n')
        idx_2 = list.index('\n', idx_1 + 1)
        bot.send_message(message.from_user.id, list[ : idx_2])
    except:
        init_web1(message)
    globals.right_ans = list[idx_2 + 1 : ]
    curr_ans.append(globals.right_ans)
    bot.send_message(message.from_user.id, 'Когда захочешь закончить игру, напиши \stop')
    bot.send_message(message.from_user.id, 'Напиши свой вариант продолжения')
        #msg = globals.bot.send_message(message.from_user.id, 'у тебя осталось 15 секунд')
    bot.register_next_step_handler(message, game)
        #for i in range(0, 15):
        #    globals.time.sleep(1)
        #    globals.bot.edit_message_text(chat_id = message.from_user.id, message_id = msg.message_id, text = 'У тебя осталось ' + str(15 - i) + ' секунд')

def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
  menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
  if header_buttons:
    menu.insert(0, header_buttons)
  if footer_buttons:
    menu.append(footer_buttons)
  return menu

def game(message = None):
    if message.text == '\stop':
        bot.send_message(message.from_user.id, 'Заканчиваю игру')
        return
    curr_ans.append(message.text)
    random.shuffle(curr_ans)
    bot.send_message(message.from_user.id, 'вот они все варианты, слева направо')
    i = 1
    for item in curr_ans:
        bot.send_message(message.from_user.id, 'вариант ' + str(i) + ' : ' + str(item))
        i += 1
    #button_list = []
    #for i in range(0, len(curr_ans)):
    #    button_list.append(types.InlineKeyboardButton('Голосую за вариант ' + str(i + 1), callback_data = i + 1))
    #reply_markup = types.InlineKeyboardMarkup(build_menu(button_list, n_cols = 1))
    bot.send_message(message.from_user.id, 'Начинается этап голосования. У тебя есть 15 секунд, чтобы выбрать вариант, который ты считаешь верным. Напиши номер варианта') #reply_markup = reply_markup)
    msg = bot.send_message(message.chat.id, 'у тебя осталось 15 секунд')
    bot.register_next_step_handler(message, i_love_democracy)
    #for i in range(0, 15):
    #    globals.time.sleep(1)
    #    globals.bot.edit_message_text(chat_id = message.chat.id, message_id = msg.message_id, text = 'У тебя осталось ' + str(15 - i) + ' секунд')

def i_love_democracy(message):
    ans = curr_ans.index(globals.right_ans) + 1
    if message.text == '\stop':
        bot.send_message(message.from_user.id, 'Заканчиваю игру')
        return
    try:
        if int(message.text) == ans:
            player.score += 1
    except:
        bot.send_message(message.from_user.id, 'лошара, по цифре попасть не смог))')
    a = ''
    for item in player_list:
        a += item.name + ' : ' + str(item.score) + '\n'
    a += 'правильный ответ :' + str(ans)
    bot.send_message(message.from_user.id, a)
    bot.send_message(message.from_user.id, 'напиши любой символ, чтобы продолжить.')
    curr_ans.clear()
    ref_list.clear()
    bot.register_next_step_handler(message, init_web)

#сделать кнопки с URL, чтобы можно было выбирать поэта