import telebot
import config
import os, sys
from requests.exceptions import ConnectionError, ReadTimeout
import random
from telebot import types
from filework import FileWork

# ваш код



MAX_LENGTH = 4096
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(content_types=['document'])
def send_text(message):
    try:
        try:
            save_dir = "C:\\GrandBiblioteka\\new\\"
        except:
            save_dir = os.getcwd()
            s = "[!] you aren't entered directory, saving to {}".format(save_dir)
            bot.send_message(message.chat.id, str(s))
        file_name = message.document.file_name
        file_id = message.document.file_name
        file_id_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_id_info.file_path)
        src = file_name
        with open(save_dir + "/" + src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, "[*] File added:\nFile name - {}\nFile directory - {}".format(str(file_name), str(save_dir)))
        file_path = os.path.join(str(save_dir), str(file_name))
        bot.send_message(message.chat.id, "{}".format(file_path))
        file = FileWork(file_path)
        file.move_to_folder(save_dir)
    except Exception as ex:
        bot.send_message(message.chat.id, "[!] error - {}".format(str(ex)))


@bot.message_handler(commands=['start'])
def send_start(message):
	current_file = os.path.realpath('main.py')
	folder_path1 = os.path.dirname(current_file)
	folder_path = os.path.join(folder_path1, 'biblioteka')
	# print(folder_path)
	files = os.listdir(folder_path)
	n_files = len(files)
	#bot.send_message(message.chat.id, f"Данный бот является хранилищем книг. На данный момент он содержит {n_files} книг жанра фентези и фантастики")

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	btn1 = types.KeyboardButton("/start")
	btn2 = types.KeyboardButton("/help")
	btn3 = types.KeyboardButton("/random")
	markup.add(btn1, btn2, btn3)
	bot.send_message(message.chat.id, text=f"Данный бот является хранилищем книг. "
										   f"На данный момент он содержит {n_files} книг жанра фентези и фантастики", reply_markup=markup)


@bot.message_handler(commands=['help'])
def send_help(message):
	bot.send_message(message.chat.id, "Для того что бы скачать нужную книгу просто напишите имя автора или слово содержащееся в названиии, "
									  "этого будет достаточно, команда рандом выводит название 10 случайных книг. Также можно добавлять "
									  "книги в библиотеку как архивом с 1 книгой, так и просто файлом в формате fb2.")

@bot.message_handler(commands=['random'])
def send_random(message):
	current_file = os.path.realpath('main.py')
	folder_path1 = os.path.dirname(current_file)
	folder_path = os.path.join(folder_path1, 'biblioteka')
	# print(folder_path)
	files = os.listdir(folder_path)
	random_files = random.sample(files, 10)
	#my_string = '\n'.join(str(random_files))
	#bot.send_message(message.chat.id, my_string)

	for file1 in random_files:
		bot.send_message(message.chat.id, file1)
	#	with open(file1, 'rb') as file:
	#		bot.send_document(message.chat.id, file)

@bot.message_handler(func=lambda message: message.chat.username in config.user_name)
def download(message):

	text1 = message.text
	print(text1)
	current_file = os.path.realpath('main.py')
	folder_path1 = os.path.dirname(current_file)
	folder_path = os.path.join(folder_path1, 'biblioteka')
	# print(folder_path)
	files = os.listdir(folder_path)
	# print(files)
	try:
		matching_files = [os.path.join(folder_path, file) for file in files if text1.lower() in file.lower()]
		file_list = '\n'.join(matching_files)  # Преобразуем список файлов в одну строку с переносами
		# print (file_list)
		# bot.send_message(message.chat.id, file_list)
		file_found = False  # Устанавливаем флаг "Файл найден" в исходное состояние

		# Проверяем каждый файл из списка
		file_found = False
		for file_path in matching_files:
			if os.path.exists(file_path):
				with open(file_path, 'rb') as file:
					bot.send_document(message.chat.id, file)
					file_found = True  # Устанавливаем флаг "Файл найден"

		# Если файл не найден, отправляем сообщение
		if not file_found:
			bot.send_message(message.chat.id, "Файл не найден.")
			print("не найдено")


	except:
		bot.send_message(message.chat.id, "не нашел")

	if (message.text == "/help"):
		bot.send_message(message.chat.id, "Для того что бы скачать нужную книгу просто напишите имя автора или слово содержащееся в названиии, этого будет достаточно")
	elif (message.text == "/random"):
		current_file = os.path.realpath('main.py')
		folder_path1 = os.path.dirname(current_file)
		folder_path = os.path.join(folder_path1, 'biblioteka')
		# print(folder_path)
		files = os.listdir(folder_path)
		random_files = random.sample(files, 10)
		#my_string = '\n'.join(str(random_files))
		for file1 in random_files:
			bot.send_message(message.chat.id, file1)


try:
	bot.infinity_polling(timeout=10, long_polling_timeout=5)
except (ConnectionError, ReadTimeout) as e:
	sys.stdout.flush()
	os.execv(sys.argv[0], sys.argv)
else:
	bot.infinity_polling(timeout=10, long_polling_timeout=5)
