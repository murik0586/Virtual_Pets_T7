from entity.Pet import Pet

class PetInteractionUI:
    def __init__(self, pet: Pet):
        self._pet = pet

    def run(self):
        while self._pet.state.is_alive:
            self._show_menu()
            choice = input("Выберите действие: ")

            match choice:
                case "1":
                    self._pet.feed()
                case "2":
                    self._pet.stroke()
                case "3":
                    self._pet.give_treat()
                case "4":
                    self._pet.walk()
                case "5":
                    self._pet.ignore()
                case "0":
                    return
                case _:
                    print("Неверный ввод!")

            print(f"\n{self._pet.state}")

        print(f"{self._pet.name} умер...")

    def _show_menu(self):
        print(f"\n--- Меню питомца {self._pet.name} ---")
        print("1. Покормить")
        print("2. Погладить")
        print("3. Дать вкусняшку")
        print("4. Погулять")
        print("5. Игнорировать")
        print("0. Назад")