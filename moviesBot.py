from telebot import TeleBot
from telebot import types
import sys

sys.path.insert(0, "./function/config")
from config import bot, myId, herId

sys.path.insert(0, "./function")
sys.path.insert(0, "./function/libraries/")
from addMovie import add_movie
from getRandomMovie import get_movie
from getListMovies import get_list_movies



@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, text = "Что-то хотели?", reply_markup = buttonControlsMenu())

@bot.message_handler(commands = ['but'])
def start(message):
    bot.send_message(message.chat.id, text = "Кнопи опять в чате", reply_markup = buttonControlsMenu())

@bot.message_handler(content_types = ['text'])
def func(message):
    if(not((message.chat.id == myId) or (message.chat.id == herId))):
        bot.send_message(message.chat.id, text = "Вы неподходите, блэаt")
        return 0

    message.text = message.text.lower()

    if(message.text == "добавить кино" or message.text == "дк" or message.text == "dk"):
        add_movie(message)

    elif(message.text == "выбрать фильм рандомно" or message.text == "вфр" or message.text == "grm"):
        get_movie(message)

    elif(message.text == "выбрать фильм из списка" or message.text == "вфс" or message.text == "glm"):
        get_list_movies(message, 0)

    elif(message.text == "бросить монетку" or message.text == "бм" or message.text == "c"):
        TossCoin(message)

    # elif(message.text == "справка" or message.text == "с"):
    #     Reference(message)

    else:
        bot.send_message(message.chat.id, text = "Я так не можу!")


def buttonControlsMenu():
    buttonControls = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    newNovie = types.KeyboardButton("Добавить кино")
    randomMovie = types.KeyboardButton("Выбрать фильм рандомно")
    specificMovie = types.KeyboardButton("Выбрать фильм из списка")
    tosscoin = types.KeyboardButton("бросить монетку")
    reference = types.KeyboardButton("Справка")
    buttonControls.add(newNovie, randomMovie, specificMovie, tosscoin)
    return buttonControls
    
import random
def TossCoin(message):
    a = random.randint(0, 100)
    if(a == 0):
        bot.send_message(message.chat.id, text = "Ребро")
    elif(a % 2):
        bot.send_message(message.chat.id, text = "Орел")
    else:
        bot.send_message(message.chat.id, text = "Решка")

bot.polling(none_stop=True)

# Возможно все таки сделать справку, но пока не особо нужна
# Возможно делать кнопку которая все останавливает каким либо образом, может просто сделать так чтобы она обрабатывалась выдавала исключение и удаляла лищние строку но тут я хз
