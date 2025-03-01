import os
import shutil
import zipfile
import xml.etree.ElementTree as ET


# extract_path = 'C:\\GrandBiblioteka\\new\\'

class FileWork:

    def __init__(self, file_path):
        self.file_path = file_path
        self.extract_path = os.path.join(os.getcwd(), 'new')
        self.folder_path = os.path.join(os.getcwd(), 'new')
        self.file_path1 = None
        self.folder_path_biblioteka = os.path.join(os.getcwd(), 'biblioteka')
        self.new_file_name = None
        self.new_file_path = None

    def is_archive(self):
        return zipfile.is_zipfile(self.file_path)

    def extract_archive(self):  # file_path, extract_path
        with zipfile.ZipFile(self.file_path, 'r') as archive:
            archive.extractall(self.extract_path)
        print(f"Archive '{self.file_path}' extracted to '{self.extract_path}'.")

    def path_to_archive(self, file_path):
        with zipfile.ZipFile(self.file_path, 'r') as archive:
            info = archive.namelist()
        print(f'Имя файла {info[0]}')
        self.file_path1 = os.path.join(self.folder_path, info[0])
        print(self.file_path1)
        return self.file_path1

    def file_rename(self):
        try:
            tree = ET.parse(self.file_path1)
        except ET.ParseError as e:
            print(f"Ошибка при обработке файла {self.file_path1}: {e}")

        root = tree.getroot()
        try:
            namespaces = {'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0'}
            title = root.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}book-title', namespaces).text
            author_element = root.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}author')
            try:
                first_name = author_element.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}first-name').text
                last_name = author_element.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}last-name').text
            except:
                print(f"пусто: {first_name} {last_name}")

            self.new_file_name = title.replace(':', '-').replace('#', '_').replace('/', '_').replace('"', '_').replace(
                '', '').replace('\n', '_').replace('*', '').replace('.', ' ').replace('?', '') + ' ' + str(
                first_name) + ' ' + str(last_name) + '.fb2'
            print(f'Фаил переименнован в {self.new_file_name}')
            self.new_file_path = os.path.join(self.folder_path, self.new_file_name)
            print(self.new_file_path)
            os.rename(self.file_path, self.new_file_path)
        except Exception as e:
            print(f"Ошибка при обработке файла {self.file_path1}: {e}")
            print("Имя файла:", self.new_file_name)

    def file_rename1(self, file_path):
        try:
            tree = ET.parse(self.file_path)
        except ET.ParseError as e:
            print(f"Ошибка при обработке файла {self.file_path1}: {e}")

        root = tree.getroot()
        try:
            namespaces = {'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0'}
            title = root.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}book-title', namespaces).text
            author_element = root.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}author')
            try:
                first_name = author_element.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}first-name').text
                last_name = author_element.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}last-name').text
            except:
                print(f"пусто: {first_name} {last_name}")

            self.new_file_name = title.replace(':', '-').replace('#', '_').replace('/', '_').replace('"', '_').replace(
                '', '').replace('\n', '_').replace('*', '').replace('.', ' ').replace('?', '') + ' ' + str(
                first_name) + ' ' + str(last_name) + '.fb2'
            print(f'Фаил переименнован в {self.new_file_name}')
            self.new_file_path = os.path.join(self.folder_path, self.new_file_name)
            print(self.new_file_path)
            os.rename(self.file_path, self.new_file_path)
        except Exception as e:
            print(f"Ошибка при обработке файла {self.file_path1}: {e}")
            print("Имя файла:", self.new_file_name)

    def move_to_folder(self, folder_path):
        # self.folder_path = folder_path
        if self.is_archive():
            print(f'Файл {os.path.basename(self.file_path)} является архивом применяю метод extract_archive')
            self.extract_archive()
            print('Начинаю переименовывать методом file_rename')
            file_path1 = self.path_to_archive(self.file_path)
            print(file_path1)
            self.file_rename()
            print('Перемещаю в основную библиотеку')
            path_file2 = os.path.join(self.folder_path_biblioteka, self.new_file_name)
            print(path_file2)

            if os.path.exists(path_file2):
                print("Такой файл уже есть")
            else:
                shutil.move(self.new_file_path, self.folder_path_biblioteka)
                print("Файл перемещен")

            print(f"File '{path_file2}' moved to folder '{self.folder_path_biblioteka}'.")
        else:
            print(f"File '{self.file_path}' is not an archive.")
            print('Начинаю переименовывать методом file_rename')
            self.file_rename1(self.file_path)
            print('Перемещаю в основную библиотеку')
            path_file2 = os.path.join(self.folder_path, self.new_file_name)
            print(path_file2)
            shutil.move(path_file2, self.folder_path_biblioteka)
            print(f"File '{path_file2}' moved to folder '{self.folder_path_biblioteka}'.")
