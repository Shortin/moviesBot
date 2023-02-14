from telebot import TeleBot
from telebot import types

# Подключение конфигов 
import sys
sys.path.insert(1, "./config/")
from config import bot

sys.path.insert(1, "./libraries/")
from mePostgresAPI import add_new_movie
from linkParserScript import SpellCheck

# Фкция просит ввест название фильма, которое надо добавить
def add_movie(message):
	bot.send_message(message.chat.id, text = "Введите название фильма: ")	
	bot.register_next_step_handler(message, check_name_movie)


# Эта функция принимает введенное пользователем сообщение
# И через парсер проверяет на правописание
checkName = ""
stockName = ""
def check_name_movie(message):
	global checkName, stockName
	checkName = SpellCheck(message.text)
	stockName = message.text
	if(checkName != None):
		bot.send_message(message.chat.id, text = f"Возможно вы имели ввиду: {checkName}?", reply_markup = buttonCheckName())
	else:
		add_movie_toBD(message, True)


# Функция добавляет фильм в бд
def add_movie_toBD(message, check):
	if(check):
		bot.send_message(message.chat.id, text = add_new_movie(stockName))
		print(f'добавлен фильм "{stockName}"')
	else:
		bot.send_message(message.chat.id, text = add_new_movie(checkName))
		print(f'добавлен фильм "{checkName}"')
		
		
# Функция кнопок
# Это кнопки проверки, они спрашивают какой вариант записать
def buttonCheckName():
    buttonCheck = types.InlineKeyboardMarkup()
    okBut = types.InlineKeyboardButton("Да, записать новый вариант", callback_data = "checkNameYes")
    notBut = types.InlineKeyboardButton("Нет, мой вариант правельный", callback_data = "checkNameNo")
    buttonCheck.add(okBut, notBut)
    return buttonCheck

# Функиця проверяет какая кнопка была выбрана
# И после выполняет заготовленые действия для той или иной кнопки
@bot.callback_query_handler(func=lambda call: call.data in ['checkNameYes', 'checkNameNo'])
def inline(call):
	if(call.data == "checkNameYes"):
		add_movie_toBD(call.message, False)
		deleteMessage(call.message, 1)		
		return

	elif(call.data == "checkNameNo"):
		add_movie_toBD(call.message, True)
		deleteMessage(call.message, 1)		
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