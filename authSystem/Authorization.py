from entity.Cat import Cat
from entity.Dog import Dog
from entity.Pets import Pets

class Authorization():
    def __init__(self, login : str, password : str):    #todo Заготовка под авторизацию, надо будет добавить сюда, вместо self.login/password = login/password, поиск логина и пароля в БД и выдавать ошибку если этих данных там нет.
        self.login = login
        self.password = password

        """Инициализирует авторизацию.
        :param login: Логин
        :param password: Пароль
        """
    def create_pet(self, nickname : str, pet: str, breed : str):
        if nickname == "":
            raise ValueError("Кличка животного не может быть пустой.")

        if pet.lower() == "cat":
            cat = Cat(nickname, breed,30)
            return cat
        elif pet.lower() == "dog":
            dog = Dog(nickname, breed,30)
            return dog
        else:
            raise ValueError("Не существует такого вида домашнего питомца.")

    def remove_pet(self, pet: Pets): #todo После добавления БД надо будет дописать функцию.
        return f"Домашний питомец {pet.nickname} удален"

    def change_pet_nickname(self, pet: Pets, new_nickname : str):
        if new_nickname != "":
            pet.nickname = new_nickname
        else:
            raise ValueError("Кличка животного не может быть пустой.")