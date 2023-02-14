from telebot import TeleBot
from telebot import types

# Подключение конфигов 
import sys
sys.path.insert(1, "./config/")
from config import bot

sys.path.insert(1, "./libraries/")
from mePostgresAPI import select_data_row, numbers_rows, move_movie
from linkParserScript import printLink

# Функция выводит список в котором можно выбрать фильм
# После выбора фильма функция выводит ссылку на него
def get_list_movies(message, num):
    bot.send_message(message.chat.id, text = "Пару секунд...")
    arrayMovies = select_data_row("new_movies")
    bot.send_message(message.chat.id, text = "Список фильмов:", reply_markup = buttonPrintFullMovie(arrayMovies, num))

# Это наши кнопочки
# Функция выводит кнопки с фильмами, а так же кнопку для того чтобы листать страницы
def buttonPrintFullMovie(arrayMovies, num):
    buttonPrint = types.InlineKeyboardMarkup()
    i = num
    while(i < len(arrayMovies)):
        if(i == num + 5 and i != len(arrayMovies)):
            buttonPrint.add(types.InlineKeyboardButton("Вывести еще?", callback_data = "newList"))
            break
        buttonPrint.add(types.InlineKeyboardButton(str(arrayMovies[i][1]), callback_data = "sM" + str(i)))
        i += 1
        if(i   == len(arrayMovies)):
            buttonPrint.add(types.InlineKeyboardButton("В начало списка?", callback_data = "newStartList"))
            break
    return buttonPrint


# Функиця проверяет какая кнопка была выбрана
# И после выполняет заготовленые действия для той или иной кнопки
numList = 0
@bot.callback_query_handler(func=lambda call: call.data )
def inline(call):
    if(call.data == "newList"):
        global numList 
        numList += 1
        deleteMessage(call.message, 2)
        get_list_movies(call.message, numList*5)       
        return
    elif(call.data == "newStartList"):
        deleteMessage(call.message, 2)
        numList = 0
        get_list_movies(call.message, 0) 
        return
    else:
        num = call.data.split("sM")[1]
        arrayMovies = select_data_row("new_movies")
        nameMovie = arrayMovies[int(num)]
        get_movie(call.message, nameMovie[1])
        return

# Функция Выводит выбраный фильм пользователю и переносит его в таблицу просмотренх
def get_movie(message, nameMovie):
    try:
        deleteMessage(message, 2)
        bot.send_message(message.chat.id, text = "Готовлю ссылочку для вас...")
        check = printLink(nameMovie)
        if(check != None):
            deleteMessage(message, 1)
            bot.send_message(message.chat.id, text=nameMovie.format(message.from_user), reply_markup=buttonLinkMovie(nameMovie))
            move_movie(nameMovie)
    except:
        bot.send_message(message.chat.id, text = "Что-то пошло не так, попробуйте еще раз")
        print("что-то в функции  get_movie(getListMovies) сломалось")
        return

# Это наши кнопочки
# Эти кнопки выводят ссылки фильмов на экран
def buttonLinkMovie(nameMovies):
    arrayLink = printLink(nameMovies)
    buttonLink = types.InlineKeyboardMarkup()
    googleBut = types.InlineKeyboardButton("Гугл", url=arrayLink[0])
    yandexBut = types.InlineKeyboardButton("Яндекс", url=arrayLink[1])
    kinopoiskBut = types.InlineKeyboardButton("Кинопоиск", url=arrayLink[2])
    buttonLink.add(googleBut, yandexBut, kinopoiskBut)
    return buttonLink

# Функция удаляет введеное количество сообщений
def deleteMessage(message, num):
    try:
        i = 0
        num += 1
        while(i + 1 < num):
            bot.delete_message(message.chat.id, message.message_id - i)
            i += 1
    except:                 
        return False
