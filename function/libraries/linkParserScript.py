from bs4 import BeautifulSoup as bs
import requests
import re 
from datetime import datetime


# Функция создает ссылку на поиск в поисковых системах, а так же ссылку на фильм на кинопоиске
def printLink(name):
	conclusion = SplittingWords(name)
	# Выводятся все поисковые ссылки
	googleLink = "https://www.google.com/search?q=" + conclusion + "+смотреть+онлайн"
	yandexLink = "https://yandex.ru/search/?text="+ conclusion + "+смотреть+онлайн"
	kinopoiskLink = "https://www.kinopoisk.ru/index.php?kp_query="+conclusion
	
	kinopoiskLink = ParserMoviesKinopoisk(kinopoiskLink)

	arrayLink = [googleLink, yandexLink, kinopoiskLink]
	return arrayLink


# Функция получает ссылку на фильм на кинопоиске, если он есть
def ParserMoviesKinopoisk(link):
	kinopoiskLink = link
	try:
		# парсятся данные о фильме с кинопоиска
		response = requests.get(kinopoiskLink)
		soup = bs(response.content, 'html.parser')
		movies = soup.find('p', class_='name')

		# из данных о фильме выбирается id и составляеся ссылка
		movies = str(movies).split()
		movies = re.findall('\d+', movies[3] )
		kinopoiskLink = "https://www.kinopoisk.ru/film/" + str(movies[0]) + "/"
	except IndexError:
		# если скрипт ловит капчу, или не находит нужный фильм происходит исключение
		# поэтому отправляется ссылка на поиск, а не на фильм для ручной обработки сайта
		kinopoiskLink = link
	return kinopoiskLink


# Функция ищет название в интернете и отправляет в функцию для нормализации
# Функция нужна для для проверки правописания
def SpellCheck(name):
	try:
		conclusion = SplittingWords(name)
		link = "https://www.google.com/search?q=" + conclusion + "+Смотреть"
		data = Parser('h3', None,  link)		
		return Filter(name, data)
	except:
		print(f'Произошла ошибка в функции SpellCheck  в {datetime.now()}, при данных: \nимя  =  {name}\n link = {link}\n data = {data}')		
		return None

# Функция перобразует строку, для поиска(смотреть онлайн => смотреть+онлайн)
def SplittingWords(name):
	name = name.split()
	conclusion = ""
	for i in range(len(name)):
		conclusion += name[i] + "+"
	conclusion = conclusion[:-1]
	return conclusion

# Функция парсит данные по ссылке 
def Parser(symbol, clas, link):
	try:
		response = requests.get(link)
		soup = bs(response.content, 'html.parser')
		if(clas == None):
			data = soup.find(symbol)
		else:
			data = soup.find(symbol, class_=clas)
		return data
	except:
		print(f'Произошла ошибка в функции Parser  в {datetime.now()}, при данных: \nsymbol  =  {symbol}\n clas = {clas}\n link = {link}')		
		return None


# функция отфильтровывает все ненужные слова и символы из полученой строки
def Filter(name, data):
	name = name.strip().lower()
	expectedName = str(data).lower()
	expectedName = re.findall(r'>([^><]+)<', expectedName)[0]#выбираются данные между >...<
	
	# Идет проверка на самые распространеные символы и слова после названия и после удаляются
	splitArray = [r' - ', r' — ', r'[(]',  r'\d\d\d\d',  r'все части', r'смотреть онлайн', r'все сезоны', r'все сезон', r'фильм']
	for i in range(len(splitArray)):
		expectedName = re.split(splitArray[i], expectedName)
		if(len(expectedName) == 2 and i > 3):
			expectedName = expectedName[1]
		else:
			expectedName = expectedName[0]
		expectedName = expectedName.strip()

	try:
		expectedName = re.findall('.*' + 'сезон', expectedName)[0]
	except:
		k = 1

	# Сравнение, если фильмы одинаковые или фильм не найден то выводит ноне, 
	# иначе выводит фильм и должен предложить пользователю
	if(str(name) == str(expectedName)):
		return None
	elif(expectedName == ""):
		return None
	else:
		return expectedName