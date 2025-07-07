import pickle

from config.settings import FILE_PATH


class Node:
    def __init__(self, position = None, value = None):
        self.position = position
        self.value = value
        self.children = []

    def __str__(self):
        return f"position: {self.position}, value: {self.value}, children: [{len(self.children)}]"

    def add_child(self, child_node):
        self.children.append(child_node)

    # Метод для сохранения объекта в файл
    def save(self):
        """Сохраняет объект в файл с обработкой ошибок записи"""
        try:
            with open(FILE_PATH, 'wb') as file:
                pickle.dump(self, file)
                print(f"Дерево загружено в файл")
            return True
        except (PermissionError, IOError) as e:
            print(f"Ошибка сохранения: {str(e)}")
            return False

    # Статический метод для загрузки объекта из файла
    @staticmethod
    def load():
        """Загружает объект из файла с обработкой ошибок"""
        try:
            with open(FILE_PATH, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            print(f"Файл {FILE_PATH} не найден.")
            return None
        except (PermissionError, IOError) as e:
            print(f"Ошибка доступа к файлу: {str(e)}")
            return None
        except (pickle.UnpicklingError, EOFError) as e:
            print(f"Ошибка чтения файла: {str(e)}")
            return None