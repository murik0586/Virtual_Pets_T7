from pymongo import MongoClient
from pymongo.results import InsertOneResult

from authSystem.Hash_token import Hash_token


class MongoDBClient:
    def __init__(self, uri : str, db_name : str):
        self.client = MongoClient(uri) #Создание подключения.
        self.db = self.client[db_name] #Поиск и выбор нужной БД.

    '''Добавление данных в коллекцию БД.
    collection_name - Наименование коллекции,
    document - Набор данных.'''
    def insert_one(self, collection_name : str, document) -> InsertOneResult:
        collection = self.db[collection_name]

        return  collection.insert_one(document)

    '''Получение всех данных из коллекции БД.
    collection_name - Наименование коллекции.'''
    def get_all(self, collection_name : str) -> list:
        collection = self.db[collection_name]

        return list(collection.find())

    '''Обновление одной записи, 
    collection_name - Наименование коллекции, 
    query  {dict} - Условие поиска(например, {"name": "Alice"}),
    new_values {dict} - Новые значения полей (например, {"age": 31, "status": "active"})'''
    def update_one(self, collection_name : str, query, new_values):
        collection = self.db[collection_name]
        return collection.update_one(query, {"$set": new_values})

    '''Поиск данных по полю field и значению value.
    collection_name - Наименование коллекции,
    field - Поле,
    value - Значение.'''
    def find_by_field(self, collection_name : str, field : str, value):
        collection = self.db[collection_name]

        return  collection.find_one({field, value})

    '''Поиск пользователя в БД по логину.
    collection_name - Наименование коллекции,
    username - логин пользователя'''
    def find_user(self, collection_name : str, username : str):
        collection = self.db[collection_name]

        return collection.find_one({"username": username})

    def create_user(self, collection_name : str, username : str, password : str) -> bool:
        collection = self.db[collection_name]
        hash_token = Hash_token()

        if collection.find_one({"username": username}):
            return False #Если уже есть пользователь с таким username, возвращаем False.

        collection.insert_one({"username": username, "password": hash_token.hash_password(password), "userGuid": hash_token.generate_guid()})

        return True

    '''Завершение подключения к mongodb.'''
    def close(self):
        self.client.close()