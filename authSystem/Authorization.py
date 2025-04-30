
class Authorization():
    def __init__(self, login : str, password : str):    #todo Заготовка под авторизацию, надо будет добавить сюда, вместо self.login/password = login/password, поиск логина и пароля в БД и выдавать ошибку если этих данных там нет.
        self.login = login
        self.password = password