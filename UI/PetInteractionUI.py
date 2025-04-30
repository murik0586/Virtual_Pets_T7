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
                    print("Ты покормил питомца")
                case "2":
                    self._pet.stroke()
                    print("Ты погладил питомца")
                case "3":
                    self._pet.give_treat()
                    print("Ты дал вкусняшку питомцу")
                case "4":
                    self._pet.walk()
                    print("Ты погулял с питомцем, а он у тебя с поводком?")
                case "5":
                    self._pet.ignore()
                    print("Ты конечно проигнорировал питомца, ну ты че!")
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