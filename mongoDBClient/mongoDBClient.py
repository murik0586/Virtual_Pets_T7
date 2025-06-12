from pymongo import MongoClient

class MongoDBClient:
    def __init__(self, url, db_name):
        self.client = MongoClient(url) #Создание подключения.
        self.db = self.client[db_name] #Поиск и выбор нужной БД.

    '''Добавление данных в таблицу БД.
    table_name - Наименование таблицы,
    data - Набор данных.'''
    def insert_one(self, table_name, data):
        table = self.db[table_name]

        return  table.insert_one(data)

    '''Получение всех данных из таблицы БД.
    table_name - Наименование таблицы.'''
    def get_all(self, table_name):
        table = self.db[table_name]

        return list(table.find())

    '''Поиск данных по полю field и значению value.
    table_name - Наименование таблицы,
    field - Поле,
    value - Значение.'''
    def find_by_field(self, table_name, field, value):
        table = self.db[table_name]

        return  table.find_one({field, value})

    '''Завершение подключения к mongodb.'''
    def close(self):
        self.client.close()