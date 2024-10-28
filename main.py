"""Проблема презеаписи zip-архива"""
import os
from zipfile import ZipFile

ROOT_DATA = "data/"


def open_file(name: str) -> bytes:
    """Открывает файл и возвращает его содержимое в виде байтов."""
    with open(ROOT_DATA + name, "rb") as file:
        return file.read()


def generate_data(files_names: list[str]) -> list[tuple[str, bytes]]:
    """Генерирует список кортежей (имя файла, байтовые данные) из списка имен файлов."""
    return [(f, open_file(f)) for f in files_names]


def write_archive(name: str, data_bite: list[tuple[str, bytes]]) -> None:
    """Добавляет данные в архив без возврата объекта ZipFile."""
    if not os.path.exists(name):
        with ZipFile(name, "w") as myzip:
            pass

    # Открываем архив один раз для добавления всех файлов
    with ZipFile(name, "a") as myzip:
        for db in data_bite:
            file_name = db[0]
            file_data = db[1]
            with open(file_name, 'wb+') as file:
                file.write(file_data)
            myzip.write(file_name)
            os.remove(file_name)


def create_archive(name: str, data_bite: list[tuple[str, bytes]]) -> ZipFile:
    """Создает архив и добавляет в него файлы, возвращает ZipFile для чтения."""
    if os.path.exists(name):
        return ZipFile(name, "r")  # Возвращаем архив для чтения, если он существует
    else:
        write_archive(name, data_bite)
        return ZipFile(name, "r")  # Возвращаем архив после создания


# Пример использования
list_files_names: list[str] = os.listdir(ROOT_DATA)
print(list_files_names)

# Генерация данных
data: list[tuple[str, bytes]] = generate_data(list_files_names)

# Создание архива
create_archive("data.zip", data)
