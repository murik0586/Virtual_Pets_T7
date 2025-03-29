from authSystem.Authorization import Authorization

# Здесь настроим пример базовой работы

# Тестирование функции создания питомца.

login = input("Введите логин: ")
password = input("Введите пароль: ")

auth = Authorization(login, password)

nickname = input("Введите кличку животного: ")
pet = input("Выберите тип животного:\n\t1)Кот\n\t2)Собака\n\n")

if pet == "1":
    cat = auth.create_pet(nickname,"cat","Бенгал")
    print(cat.nickname)
elif pet == "2":
    dog = auth.create_pet(nickname, "dog", "Овчарка")
    print(dog.nickname)
else:
    raise ValueError("Указано некорректное значение.")