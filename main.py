from entity.Cat import Cat
from entity.Dog import Dog

# Здесь настроим пример базовой работы

# todo Влад - нужна функция создания питомца
pet_one = Cat("Вальтер", "Бенгал", points_health=30, happiness_indicator=15)
pet_two = Dog("Рэкс", "Овчарка", points_health=30, happiness_indicator=15)
pet_one.hunger_level = 10
print(pet_one)
print(pet_two)
