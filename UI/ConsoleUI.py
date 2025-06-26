import mongoDBClient.mongoDBClient
from authSystem.Authorization import Authorization
from entity.PetManager import PetManager
from UI.PetInteractionUI import PetInteractionUI
import time

class ConsoleUI:
    def __init__(self, manager: PetManager, uri : str, db_name : str):
        self._manager = manager
        self.auth = Authorization(uri, db_name)

    def run(self):
        #Вывод окна авторизации.
        while True:
            self._show_authorization()
            choice = input("Выберите действие: ")

            match choice:
                case "1":
                    if self._authorization_ui() is not None:
                        break
                case "2":
                    self._registration_ui()
                case "0":
                    return
                case _:
                    print("Неверный ввод!")

        while True:
            self._show_main_menu()
            choice = input("Выберите действие: ")

            match choice:
                case "1":
                    self._create_pet()
                case "2":
                    self._manage_pet()
                case "3":
                    self._show_all_pets()
                case "4":
                    self._delete_pet()
                case "0":
                    return
                case _:
                    print("Неверный ввод!")

    def _show_authorization(self):
        print ("\n=== Виртуальный питомец ===")
        print("1. Авторизация")
        print("2. Регистрация")
        print("0. Выход")

    def _authorization_ui(self) -> bool:
        username = input("Введите логин: ")
        password = input("Введите пароль: ")
        return self.auth.authorize(username, password)

    def _registration_ui(self):
        username = input("Введите логин: ")
        password = input("Введите пароль: ")
        self.auth.registrate(username, password)


    def _show_main_menu(self):

        print("\n=== Виртуальный питомец ===")
        print("1. Создать питомца")
        print("2. Выбрать питомца")
        print("3. Показать всех питомцев")
        print("4. Удалить питомца")
        print("0. Выход")

    def _create_pet(self):
        name = input("Введите имя питомца: ").strip()
        try:
            health = int(input("Введите здоровье: ") or 5) #Я добавлю ребят чутка валидации!
        except ValueError:
            print("Нужно вводить число! Установлено значение по умолчанию (т.е. 5)")
            health = 5
        pet_id = self._manager.create_pet(name, health)
        print(f"Создан питомец {name} с ID {pet_id}")

    def _manage_pet(self):
        pet_id,pet = self._select_pet()
        if pet:
            PetInteractionUI(pet).run()

    def _select_pet(self):
        pets = self._manager.pets
        if not pets:
            print("Нет доступных питомцев!")
            return None, None #Внес изменения

        print("\nСписок питомцев:")
        for id_, pet in pets.items():
            print(f"ID {id_}: {pet.name}")

        pet_id = int(input("Введите ID питомца: "))
        return pet_id, self._manager.get_pet(pet_id) # здесь еще внес, кажется с id не лады были(влияло на функцию delete)

    def _show_all_pets(self):
        for id_, pet in self._manager.pets.items():
            print(f"\nID {id_}:")
            print(pet)

    def _delete_pet(self):
        pet_id,pet = self._select_pet() #раз ты тут, id у тебя было объекта, а не питомца)
        if pet and self._manager.remove_pet(id(pet_id)):
            print(f"Питомец {pet.name} удален")