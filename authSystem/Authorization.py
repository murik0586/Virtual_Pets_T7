import mongoDBClient.mongoDBClient
from authSystem.Hash_token import Hash_token
from mongoDBClient import mongoDBClient

class Authorization:
    def __init__(self, uri : str, db_name : str):
        self.uri = uri
        self.db_name = db_name
        self.mongo_client = mongoDBClient.MongoDBClient(
            uri=uri,
            db_name=db_name,
            username="admin",
            password="12345"
        )

        """Инициализирует авторизацию.
        :param login: Логин
        :param password: Пароль
        """
    def authorize(self, username : str, password : str):
        hash_token = Hash_token()

        user = self.mongo_client.find_user("users", username)
        if user and user['password'] == hash_token.hash_password(password):
            return user.get("userGuid")
        else:
            print(f"Пользователя с таким {username} не существует.")
            return None

    def registrate(self, username : str, password : str):
        user_status = self.mongo_client.create_user("users", username, password)

        if user_status == False:
            print(f"Пользователь {username} уже существует.")
            return False

        print(f"Пользователь с {username} успешно создан.")
        return True
