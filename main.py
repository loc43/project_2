import branch_1
import branch_2
import globals
from globals import player
from telebot import types

bot = globals.bot
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        globals.user_list.append(message.from_user.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('ИГРА')
        btn2 = types.KeyboardButton('ПРАВИЛА')
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, 'Привет. Я бот для игры в стихотворную завалинку. Если хочешь сыграть, напиши мне ИГРА, если хочешь узнать правила -- ПРАВИЛА', reply_markup = markup)
        bot.register_next_step_handler(message, rules)

def rules(message):
    if message.text == 'ИГРА':
        bot.register_next_step_handler(message, get_name)
        bot.send_message(message.from_user.id, 'как тебя зовут?')
    if message.text == 'ПРАВИЛА':
        bot.send_message(message.from_user.id, 'Ведущий выбирает слово из официального источника энциклопедической направленности.' +
                        'Каждый участник (или команда) пишет вариант энциклопедической статьи для выбранного слова, в то время как ведущий адаптирует и сокращает настоящий вариант.' + 
                        'После того, как Ведущий зачитал все статьи, включая правильную, в произвольном порядке, игроки отдают свой голос той или иной статье.')
        bot.register_next_step_handler(message, rules)


def get_name(message):
    if message.text in globals.player_names:
        bot.send_message(message.from_user.id, 'кажется, это имя уже занято. попробуй еще раз.')
        bot.register_next_step_handler(message, get_name)
    else:
        globals.player_names.append(message.text)
        player.name = message.text
        globals.player_list.append(player)
        bot.send_message(message.from_user.id, 'из какой ты команды?')
        bot.register_next_step_handler(message, get_team)

def get_team(message):
    player.team = message.text
    bot.send_message(message.from_user.id, 'ты ' + player.name + ' из команды ' + player.team)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('ИГРАТЬ С КОМПЬЮТЕРОМ И ДРУЗЬЯМИ')
    btn2 = types.KeyboardButton('ИГРАТЬ С ДРУЗЬЯМИ')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, 'выбери, как хочешь играть', reply_markup = markup)
    bot.register_next_step_handler(message, level1)

def level1(message):
    global comp
    if message.text == 'ИГРАТЬ С КОМПЬЮТЕРОМ И ДРУЗЬЯМИ':
        comp = True
        branch_1.init_comp(message)
    else:
        comp = False
        branch_2.init_web(message)
    
    

bot.polling(none_stop=True, interval=0)


