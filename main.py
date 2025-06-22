from authSystem.Authorization import Authorization
from entity.PetManager import PetManager
from UI.ConsoleUI import ConsoleUI

if __name__ == "__main__":
    manager = PetManager()
    ui = ConsoleUI(manager, "mongodb://localhost:27017/", "tamagotchi_db")
    ui.run()