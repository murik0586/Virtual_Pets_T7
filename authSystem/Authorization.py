from entity.Pet import Pet
from entity.PetFactory import PetFactory

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
            cat = PetFactory.create_pet('cat')
            return cat
        elif pet.lower() == "dog":
            dog = PetFactory.create_pet('dog')
            return dog
        else:
            raise ValueError("Не существует такого вида домашнего питомца.")

    def remove_pet(self, pet: Pet): #todo После добавления БД надо будет дописать функцию.
        return f"Домашний питомец {pet.name} удален"

    def change_pet_name(self, pet: Pet, name : str):
        if name != "":
            pet.name = name
        else:
            raise ValueError("Кличка животного не может быть пустой.")