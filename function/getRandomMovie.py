from telebot import TeleBot
from telebot import types

# Подключение конфигов 
import sys
sys.path.insert(1, "./config/")
from config import bot

sys.path.insert(1, "./libraries/")
from mePostgresAPI import print_random_movie, move_movie
from linkParserScript import printLink

# Функция возвращает в чат рандомный фильм из бд,  а так же переносит его в таблицу просмотреных фильмв
checkMovie = None
def get_movie(message):
	global checkMovie
	while(1):
		movie = print_random_movie()
		if(movie == False):
			print("Функця не вернула фильм(")
			return "Что-то пошло не так\nПопробуйте еще раз"
		if(checkMovie == None):
			checkMovie = movie
		elif(checkMovie != movie):
			checkMovie = movie
			break;

	bot.send_message(message.chat.id, text = f'Сегодня фильм: "{movie}"\nВас устраивает выбранный фильм?', reply_markup = buttonYesNoMovie())

# Это наши кнопочки, функция просто создает и "Выводит" кнопки
def buttonYesNoMovie():
    buttonCheck = types.InlineKeyboardMarkup()
    okBut = types.InlineKeyboardButton("Все окей, Спасибо", callback_data = "yesMovie")
    notBut = types.InlineKeyboardButton("Нет, выбрать новый", callback_data = "noMovie")
    buttonCheck.add(okBut, notBut)
    return buttonCheck

# Функиця проверяет какая кнопка была выбрана
# И после выполняет заготовленые действия для той или иной кнопки
@bot.callback_query_handler(func=lambda call: call.data in ['yesMovie', 'noMovie'])
def inline(call):
	if(call.data == "yesMovie"):  
		deleteMessage(call.message, 1)
		bot.send_message(call.message.chat.id, text="Всегда пожалуйста\nСейчас сделаю ссылочку для вас, подождите пару секунд")
		bot.send_message(call.message.chat.id, text = f"Вот ваши ссылочки на фильм: {checkMovie}:", reply_markup = buttonLinkMovie(checkMovie))
		move_movie(checkMovie)
		return      

	elif(call.data == "noMovie"):
		deleteMessage(call.message, 1)
		get_movie(call.message)
		return

# Функция удаляет введеное количество сообщений
def deleteMessage(message, num):
	try:
		i = 0
		num += 1
		while(i + 1 < num):
			bot.delete_message(message.chat.id, message.message_id - i)
			i += 1
	except:
		print("Опять какие-то проблемы с удалением")
		return False

# Это наши кнопочки, эти кнопочки выводят ссылку на выбраный фильм
def buttonLinkMovie(nameMovies):
    arrayLink = printLink(nameMovies)
    buttonLink = types.InlineKeyboardMarkup()
    googleBut = types.InlineKeyboardButton("Гугл", url=arrayLink[0])
    yandexBut = types.InlineKeyboardButton("Яндекс", url=arrayLink[1])
    kinopoiskBut = types.InlineKeyboardButton("Кинопоиск", url=arrayLink[2])
    buttonLink.add(googleBut, yandexBut, kinopoiskBut)
    return buttonLink