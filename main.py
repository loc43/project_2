from globals import bot, player_dict, name_list, Player, players
from telebot import types
import globals
import initiation
#прикрутить базу данных с результатами игроков?
#добавить таймер
#прописать защиту от дурака: нельзя голосовать за себя
# reply_to вместо

name_list.append('Bot')
globals.names_dict['Bot'] = globals.machine
player_dict[0] = 'Bot'

name_list.append('Truth')
globals.names_dict['Truth'] = globals.machine
player_dict[1] = 'Truth'


@bot.message_handler(content_types=['text'])
def start_message(message):
    if globals.crunches:
        globals.chat_id = message.chat.id
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('ИГРА')
        btn2 = types.KeyboardButton('ПРАВИЛА')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Привет. Я бот для игры в стихотворную завалинку. Если хочешь сыграть, напиши мне ИГРА, если хочешь узнать правила -- ПРАВИЛА. Для того, чтобы я работал корректно, нужно, чтобы каждый из вас активировал меня в личке и написал там свое имя. ', reply_markup = markup)
        bot.register_next_step_handler_by_chat_id(globals.chat_id, step_2)
    else:
        initiation.game(message)


def step_2(message):
    if message.chat.id == globals.chat_id:
        if message.text == 'ИГРА':    
            globals.crunches = False
            bot.send_message(globals.chat_id, 'Напишите ответом на этом сообщение, как вас зовут. Когда будете готовы, напишите Играть!')
            bot.register_next_step_handler_by_chat_id(globals.chat_id, get_name)
        elif message.text == 'ПРАВИЛА':
            bot.send_message(message.chat.id, 'Ведущий выбирает слово из официального источника энциклопедической направленности.' +
                            'Каждый участник (или команда) пишет вариант энциклопедической статьи для выбранного слова, в то время как ведущий адаптирует и сокращает настоящий вариант.' + 
                            'После того, как Ведущий зачитал все статьи, включая правильную, в произвольном порядке, игроки отдают свой голос той или иной статье.')
            bot.register_next_step_handler_by_chat_id(globals.chat_id, step_2)
        else:
            bot.send_message(message.chat.id, 'Боюсь, я не понял тебя. Попробуй еще раз.')
            bot.bot.register_next_step_handler_by_chat_id(globals.chat_id, step_2)

def get_name(message):
    if message.text == 'Играть!':
        initiation.step_3()
    else:
        if message.text in name_list:
            bot.send_message(message.from_user.id, 'кажется, это имя уже занято. Попробуй еще раз.')
        else:
            bot.send_message(message.from_user.id, 'тебя зовут ' + message.text)
            name_list.append(message.text)
            player = Player()
            player.name = message.text
            player.id = message.from_user.id
            players.append(player)
            globals.names_dict[message.text] = player
            player_dict[message.from_user.id] = message.text
        bot.register_next_step_handler_by_chat_id(globals.chat_id, get_name)

bot.polling(none_stop=True, interval=0)
