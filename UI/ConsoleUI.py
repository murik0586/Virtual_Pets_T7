from entity.PetManager import PetManager
from UI.PetInteractionUI import PetInteractionUI
import time

class ConsoleUI:
    def __init__(self, manager: PetManager):
        self._manager = manager

    def run(self):
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

    def _show_main_menu(self):

        print("\n=== Виртуальный питомец ===")
        print("1. Создать питомца")
        print("2. Выбрать питомца")
        print("3. Показать всех питомцев")
        print("4. Удалить питомца")
        print("0. Выход")

    def _create_pet(self):
        name = input("Введите имя питомца: ").strip()
        health = int(input("Введите здоровье: ") or 5)
        pet_id = self._manager.create_pet(name, health)
        print(f"Создан питомец {name} с ID {pet_id}")

    def _manage_pet(self):
        pet = self._select_pet()
        if pet:
            PetInteractionUI(pet).run()

    def _select_pet(self):
        pets = self._manager.pets
        if not pets:
            print("Нет доступных питомцев!")
            return None

        print("\nСписок питомцев:")
        for id_, pet in pets.items():
            print(f"ID {id_}: {pet.name}")

        pet_id = int(input("Введите ID питомца: "))
        return self._manager.get_pet(pet_id)

    def _show_all_pets(self):
        for id_, pet in self._manager.pets.items():
            print(f"\nID {id_}:")
            print(pet)

    def _delete_pet(self):
        pet = self._select_pet()
        if pet and self._manager.remove_pet(id(pet)):
            print(f"Питомец {pet.name} удален")