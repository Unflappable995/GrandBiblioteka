import telebot
import config
import os, sys
from requests.exceptions import ConnectionError, ReadTimeout

MAX_LENGTH = 4096
bot = telebot.TeleBot(config.TOKEN)



@bot.message_handler(func=lambda message: True)
def download(message):
    text1 = message.text
    print(text1)
    current_file = os.path.realpath('main.py')
    folder_path1 = os.path.dirname(current_file)
    folder_path = os.path.join(folder_path1, 'biblioteka')
    #print(folder_path)
    files = os.listdir(folder_path)
    #print(files)
    try:
        matching_files = [os.path.join(folder_path, file) for file in files if text1.lower() in file.lower()]
        file_list = '\n'.join(matching_files)  # Преобразуем список файлов в одну строку с переносами
        #print (file_list)
        #bot.send_message(message.chat.id, file_list)
        for file_path in matching_files:
            with open(file_path, 'rb') as file:
                bot.send_document(message.chat.id, file)
    except:
        bot.send_message(message.chat.id, "не нашел")


try:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
except (ConnectionError, ReadTimeout) as e:
    sys.stdout.flush()
    os.execv(sys.argv[0], sys.argv)
else:
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
