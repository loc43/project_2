import globals
import random

#игра на 1 игрока, всегда 2 варианта

def init_comp(message):
        globals.bot.send_message(message.from_user.id, 'Когда захочешь закончить игру, напиши \stop')
        tmp = random.choice(list(globals.task))
        globals.bot.send_message(message.from_user.id, tmp)
        for id in globals.user_list:
            globals.bot.send_message(id, 'Напиши свой вариант продолжения')
        #msg = globals.bot.send_message(message.from_user.id, 'у тебя осталось 15 секунд')
        global right_ans
        right_ans = globals.task[tmp][0]
        globals.curr_ans.append(globals.task[tmp][0])
        globals.curr_ans.append(globals.task[tmp][1])
        globals.bot.register_next_step_handler(message, game)
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
        globals.bot.send_message(message.from_user.id, 'Заканчиваю игру')
        return
    globals.curr_ans.append(message.text)
    random.shuffle(globals.curr_ans)
    for id in globals.user_list:
        globals.bot.send_message(id, 'вот они все варианты, слева направо')
    i = 1
    for item in globals.curr_ans:
        for id in globals.user_list:
            globals.bot.send_message(message.from_user.id, 'вариант ' + str(i) + ' : ' + str(item))
        i += 1
    #button_list = []
    #for i in range(0, len(curr_ans)):
    #    button_list.append(types.InlineKeyboardButton('Голосую за вариант ' + str(i + 1), callback_data = i + 1))
    #reply_markup = types.InlineKeyboardMarkup(build_menu(button_list, n_cols = 1))
    for id in globals.user_list:
        globals.bot.send_message(id, 'Начинается этап голосования. У тебя есть 15 секунд, чтобы выбрать вариант, который ты считаешь верным. Напиши номер варианта') #reply_markup = reply_markup)
    print(globals.user_list)
    msg = globals.bot.send_message(message.chat.id, 'у тебя осталось 15 секунд')
    globals.bot.register_next_step_handler(message, i_love_democracy)
    #for i in range(0, 15):
    #    globals.time.sleep(1)
    #    globals.bot.edit_message_text(chat_id = message.chat.id, message_id = msg.message_id, text = 'У тебя осталось ' + str(15 - i) + ' секунд')

def i_love_democracy(message):
    ans = globals.curr_ans.index(right_ans) + 1
    if message.text == '\stop':
        globals.bot.send_message(message.from_user.id, 'Заканчиваю игру')
        return
    try:
        if int(message.text) == ans:
            globals.player.score += 1
    except:
        globals.bot.send_message(message.from_user.id, 'лошара, по цифре попасть не смог))')
    a = ''
    for item in globals.player_list:
        a += item.name + ' : ' + str(item.score) + '\n'
    a += 'правильный ответ :' + str(ans)
    globals.bot.send_message(message.from_user.id, a)
    globals.bot.send_message(message.from_user.id, 'напиши любой символ, чтобы продолжить.')
    globals.curr_ans.clear()
    globals.bot.register_next_step_handler(message, init_comp)