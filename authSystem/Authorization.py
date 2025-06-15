from authSystem.Hash_token import Hash_token
from mongoDBClient import mongoDBClient

class Authorization:
    def __init__(self, uri : str, db_name : str):
        self.uri = uri
        self.db_name = db_name

        """Инициализирует авторизацию.
        :param login: Логин
        :param password: Пароль
        """
    def authorize(self, username : str, password : str):
        database = mongoDBClient.MongoDBClient(self.uri, self.db_name)
        hash_token = Hash_token()

        user = database.find_user("Users", username)
        if user and user['password'] == hash_token.hash_password(password):
            return user.get("userGuid")
        else:
            return None # Переделать на вывод ошибки.

    def registrate(self, username : str, password : str):
        database = mongoDBClient.MongoDBClient(self.uri, self.db_name)

        user_status = database.create_user("Users", username, password)

        if user_status == False:
            print(f"Пользователь {username} уже существует.")
            return False

        print(f"Пользователь с {username} успешно создан.")
        return True
