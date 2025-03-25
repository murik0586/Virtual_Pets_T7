from entity.Cat import Cat
from entity.Pets import Pets as Pet

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
pets = Cat('1', '2', 3, 4, 5, "sfsaf")
help(pets.get_eat)
print(pets.get_eat())
pets.set_eat("10")
print(pets.get_eat())