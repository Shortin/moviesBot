import sys
sys.path.insert(1, "/home/gupik/program/whileMoviesBot/function/config")

from config import connection
cursor = connection.cursor()

import random
from datetime import datetime


# Функция возращает последний элемент id
def last_number_rows(nameTable):
	try:
		cursor.execute(f"SELECT * FROM {nameTable};")
		return cursor.fetchall()[len(cursor.fetchall())-1][0]
	except:
		print(f'Произошла ошибка в функции last_number_rows  в {datetime.now()}, при данных: \nимя таблицы = {nameTable}')
		return False

# Функция возращает количество строк в выбраной таблице
def numbers_rows(nameTable):
	try:
		cursor.execute(f"SELECT * FROM {nameTable};")
		return len(cursor.fetchall())
	except:
		print(f'Произошла ошибка в функции numbers_rows  в {datetime.now()}, при данных: \nимя таблицы = {nameTable}')
		return False

# Фукция возврщает данные из определенной таблицы
def select_data_row(nameTable):
	try:
		cursor.execute(f"SELECT * from {nameTable}")
		return cursor.fetchall()
	except:
		print(f'Произошла ошибка в функции select_data_row  в {datetime.now()}, при данных:  \nимя таблицы = {nameTable}')
		return False

# Функция добавляет данные в выбраную таблицу
def insert_row(nameTable, id, data):
	try:
		cursor.execute(f"INSERT INTO {nameTable} VALUES ({id}, '{data}')")
		connection.commit()  
		return True
	except:
		print(f'Произошла ошибка в функции insert_row  в {datetime.now()}, при данных: \nимя таблицы = {nameTable} \nid = {id} \nДанные = {data}')
		return False

# Функция обновляет данные в выбраной строке таблицы
def update_data_row(nameTable, id, newData):
	try:
		cursor.execute(f"UPDATE {nameTable} SET movies = '{newData}' WHERE id = {id}")
		connection.commit()  
		return True
	except:
		print(f'Произошла ошибка в функции update_data_row  в {datetime.now()}, при данных: \nимя таблицы = {nameTable} \nid = {id} \nНовые данные = {newData}')
		return False

# Функция обновляет id в выбраной таблице и строке
def update_id_row(nameTable, id, newId):
	try:
		cursor.execute(f"UPDATE {nameTable} SET id = '{newId}' WHERE id = {id}")
		connection.commit()  
		return True
	except:
		print(f'Произошла ошибка в функции update_data_row  в {datetime.now()}, при данных: \nимя таблицы = {nameTable} \nid = {id} \nНовый id = {newId}')
		return False

# Функция удаляет выбраную строку в выбраной таблице
def delete_row(nameTable, id):
	try:
		cursor.execute(f"DELETE FROM {nameTable} WHERE id = {id}")
		connection.commit()  
		return True
	except:
		print(f'Произошла ошибка в функции delete_row  в {datetime.now()}, при данных: \nимя таблицы = {nameTable} \nid = {id}')
		return False


# Функция добавляет фильм в таблицу
def add_new_movie(movie):
	check_none = check_movie("new_movies", movie)
	if(check_none == None):
		print(f'Произошла ошибка в функции check_none  в {datetime.now()}, она вернула None')
		return "Произошла ошибка, попробуйте еще раз(хотя скорее всего это не поможет)"
	if(check_movie("new_movies", movie)):
		return "Такой фильм уже есть!"

	id = last_number_rows("new_movies") + 1
	check = insert_row("new_movies", id, movie)
	if(check != False):
		return "Фильм успешно добавлен"
	else:
		return "Произошла ошибка, попробуйте еще раз(хотя скорее всего это не поможет)"
# Функция проверяет есть такой же фильм в бд или нет
def check_movie(nameTable, movie):
	rows = select_data_row("new_movies")
	if(rows == False):
		return None
	for row in rows:
		if(movie == row[1]):
			return True
	return False


# Функция выводит рандомный фильм из таблицы новых фильмов
def print_random_movie():
	try:
		movies = select_data_row("new_movies")
		num = random.randint(0, len(movies)-1)

		# idMovie = movies[num][0]
		movie = movies[num][1]
		# move(True, idMovie, movie)
		return movie
	except:
		print(f'Произошла ошибка в функции print_random_movie  в {datetime.now()}')
		return False

# Функция переносит выбраны фильм в столбец просмотренных
def move_movie(movie):
	try:
		rows = select_data_row("new_movies")
		id = 0
		for row in rows:
			if(movie == row[1]):
				id = row[0]
				break;
		move(True, id, movie)
		return True
	except:
		print(f'Произошла ошибка в функции move_movie  в {datetime.now()}')
		return False

# Функция возращает последни добавленный фильм из таблицы просмотрнных в таблицу новых
def return_movie():
	try:
		movies = select_data_row("viewed_movies")
		idMovie = len(movies)-1
		movie = movies[idMovie][1]
		delete_row("viewed_movies", idMovie)
		insert_row("new_movies", last_number_rows("new_movies")+1, movie)
		move(False, idMovie, movie)
		return True
	except:
		print(f'Произошла ошибка в функции return_movie  в {datetime.now()}')
		return False

# Функция мув переносит выбраный элемент тблицы "А" в конец таблицы "В"
def move(check, id, movie):
	if(check == True):
		delete_row("new_movies", id)
		insert_row("viewed_movies", last_number_rows("viewed_movies")+1, movie)
	else:
		delete_row("viewed_movies", id)
		insert_row("new_movies", last_number_rows("new_movies")+1, movie)
