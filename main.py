from entity.PetManager import PetManager
from UI.ConsoleUI import ConsoleUI

if __name__ == "__main__":
    manager = PetManager()
    ui = ConsoleUI(manager)
    ui.run()