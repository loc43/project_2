import random
from globals import bot, poets_dict
import globals
from telebot import types
import web_searcher

def step_3():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('ИГРАТЬ С КОМПЬЮТЕРОМ И ДРУЗЬЯМИ')
    btn2 = types.KeyboardButton('ИГРАТЬ С ДРУЗЬЯМИ')
    markup.add(btn1, btn2)
    bot.send_message(globals.chat_id, 'выбери, как хочешь играть', reply_markup = markup)
    bot.register_next_step_handler_by_chat_id(globals.chat_id, step_4)

def step_4(message):
    if message.text == 'ИГРАТЬ С КОМПЬЮТЕРОМ И ДРУЗЬЯМИ':
        globals.web = False
        bot.send_message(globals.chat_id, 'see ya loosers')
    else:
        globals.web = True
        bot.send_message(globals.chat_id, 'so long, suckers')
    initiation_1(message)

def init_comp(message):
    tmp = random.choice(list(globals.task))
    globals.bot.send_message(globals.chat_id, tmp)
    globals.right_ans = globals.task[tmp][0]
    globals.ans_dict[globals.task[tmp][0]] = 'Truth'
    globals.ans_dict[globals.task[tmp][1]] = 'Bot'
    globals.curr_ans.append(globals.task[tmp][0])
    globals.curr_ans.append(globals.task[tmp][1])
    initiation_2(message)

def init_web():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.register_next_step_handler_by_chat_id(globals.chat_id, init_web1)
    btn1 = types.KeyboardButton('Ахматова')
    btn2 = types.KeyboardButton('Цветаева')
    btn3 = types.KeyboardButton('Пастернак')
    btn4 = types.KeyboardButton('Бродский')
    btn5 = types.KeyboardButton('Асадов')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(globals.chat_id, 'выбери поэта', reply_markup = markup)

def init_web1(message):
    list = web_searcher.find_text(web_searcher.find_poem(poets_dict[message.text]))
    try:
        idx_1 = list.index('\n')
        idx_2 = list.index('\n', idx_1 + 1)
        bot.send_message(globals.chat_id, list[ : idx_2])
    except:
        init_web1(message)
    globals.right_ans = list[idx_2 + 1 : ]
    globals.curr_ans.append(globals.right_ans)
    globals.ans_dict[globals.right_ans] = 'Truth'
    initiation_2(message)

def initiation_1(message):
    if globals.web:
        init_web()
    else:
        init_comp(message)

def initiation_2(message):
    globals.bot.send_message(globals.chat_id, 'Когда захочешь закончить игру, напиши \stop')
    bot.send_message(globals.chat_id, 'Напиши свой вариант продолжения мне в личные сообщения')


def game(message):
    if message.text == '\stop':
        globals.bot.send_message(message.from_user.id, 'Заканчиваю игру')
        return
    if message.text == '/start':
        globals.bot.send_message(message.from_user.id, 'введи свой вариант')
        globals.bot.register_next_step_handler_by_chat_id(message.from_user.id, game)
    globals.curr_ans.append(message.text)
    globals.bot.send_message(message.from_user.id, 'твой ответ записан. ' + 'ждем еще '+ str(len(globals.players) + 2 - globals.web - len(globals.curr_ans)) + ' человек')
    print(globals.players, globals.curr_ans)
    globals.ans_dict[message.text] = globals.player_dict[message.from_user.id]
    if len(globals.curr_ans) < len(globals.players) + 2 - globals.web:
        globals.bot.register_next_step_handler(message, game)
    else:
        random.shuffle(globals.curr_ans)
        globals.bot.send_message(globals.chat_id, 'вот они все варианты, слева направо')
        i = 1
        for item in globals.curr_ans:
            globals.bot.send_message(globals.chat_id, 'вариант ' + str(i) + ' : ' + str(item))
            i += 1
        globals.bot.send_message(globals.chat_id, 'Начинается этап голосования. У тебя есть 15 секунд, чтобы выбрать вариант, который ты считаешь верным. Напиши номер варианта мне в лс') #reply_markup = reply_markup)
        globals.bot.register_next_step_handler(message, i_love_democracy)
  

def i_love_democracy(message):
    globals.ans_counter += 1
    if message.text == '\stop':
        globals.bot.send_message(globals.chat_id, 'Заканчиваю игру')
        return
    try:
        if globals.ans_dict[globals.curr_ans[int(message.text) - 1]] == 'Truth' :
            globals.names_dict[globals.player_dict[message.from_user.id]].score += 3
        else:
            globals.names_dict[globals.ans_dict[globals.curr_ans[int(message.text) - 1]]].score += 1
    except:
        globals.bot.send_message(message.from_user.id, 'кажется, ты опечатался. Попробуй еще раз.')
        bot.register_next_step_handler_by_chat_id(message.from_user.id, i_love_democracy)
    if globals.ans_counter < len(globals.players):
        globals.bot.register_next_step_handler(message, i_love_democracy)
    bot.register_next_step_handler_by_chat_id(message.from_user.id, game)
    if globals.ans_counter >= len(globals.players):
        results()

def results():
        ans = globals.curr_ans.index(globals.right_ans) + 1
        a = ''
        if not globals.web:
            a += 'Bot : ' + str(globals.machine.score) + '\n'
        for item in globals.players:
            a += item.name + ' : ' + str(item.score) + '\n'
        a += 'правильный ответ :' + str(ans)
        globals.bot.send_message(globals.chat_id, a)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('ДА')
        btn2 = types.KeyboardButton('НЕТ')
        markup.add(btn1, btn2)
        bot.send_message(globals.chat_id, 'Хотите сыграть еще раз?', reply_markup = markup)
        bot.register_next_step_handler_by_chat_id(globals.chat_id, endgame)

def endgame(message):
    if message.text == 'ДА':
        globals.curr_ans.clear()
        globals.ans_counter = 0
        globals.ans_dict.clear()
        step_3()
    else:
        return
        