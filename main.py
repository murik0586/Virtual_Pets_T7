from authSystem.Authorization import Authorization
from entity.PetManager import PetManager
from UI.ConsoleUI import ConsoleUI
from mongoDBClient.mongoDBClient import MongoDBClient
from server import TamagotchiServer

if __name__ == "__main__":
    # Создаем экземпляр MongoDB клиента
    mongo_client = MongoDBClient(
        uri="mongodb://localhost:27017/",
        db_name="tamagotchi_db",
        username="admin",
        password="12345"
    )

    # Создаем экземпляр менеджера питомцев
    manager = PetManager()

    # Создаем экземпляр сервера с передачей mongo_client
    server = TamagotchiServer(mongo_client=mongo_client)

    # Запускаем сервер в отдельном потоке (не блокирующий режим)
    server.run(block=False)

    # Выводим информацию о запущенном сервере
    print(f"Сервер запущен на порту {server.port}")
    print("Доступные эндпоинты:")
    print("- POST /auth/register - регистрация нового пользователя")
    print("- POST /auth/login - авторизация пользователя")
    print("- GET /{user_uuid}/pets - получение списка питомцев")
    print("- POST /{user_uuid}/pets - создание нового питомца")
    print("- GET /{user_uuid}/pets/{id} - получение информации о питомце")
    print("- POST /{user_uuid}/pets/{id}/{action} - выполнение действия с питомцем")
    print("- DELETE /{user_uuid}/pets/{id} - удаление питомца")

    # Запускаем консольный интерфейс
    ui = ConsoleUI(manager, "mongodb://localhost:27017/", "tamagotchi_db")

    try:
        ui.run()
    except KeyboardInterrupt:
        print("\nЗавершение работы...")
    finally:
        # Останавливаем сервер при выходе
        server.stop()
        print("Сервер остановлен")