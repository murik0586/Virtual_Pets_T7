import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse
from datetime import datetime
import logging

from authSystem.Authorization import Authorization
from entity.Pet import Pet
from entity.PetManager import PetManager
from mongoDBClient import mongoDBClient

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


class TamagotchiServer:
    def __init__(self, mongo_client=None):
        self.pet_manager = PetManager()
        if mongo_client:
            self.mongo_client = mongo_client
        else:
            self.mongo_client = mongoDBClient.MongoDBClient(
                uri="mongodb://localhost:27017/",
                db_name="tamagotchi_db",
                username="admin",
                password="12345"
            )

        # Создаем объект авторизации
        self.auth = Authorization(
            uri="mongodb://localhost:27017/",
            db_name="tamagotchi_db"
        )

        self._load_pets_from_db()
        self.httpd = None
        self.thread = None

    def run(self, port=8000, block=True):
        server_address = ('', port)
        self.httpd = HTTPServer(server_address, self.get_handler())
        self.port = self.httpd.server_port
        logger.info(f"Starting server on port {self.port}")

        if block:
            try:
                self.httpd.serve_forever()
            except KeyboardInterrupt:
                self.stop()
            finally:
                self.mongo_client.close()
        else:
            self.thread = threading.Thread(target=self.httpd.serve_forever)
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        """Остановка сервера"""
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()  # Закрываем сокет
        if self.thread:
            self.thread.join()
        # Закрываем соединение с MongoDB
        self.mongo_client.close()

    def _load_pets_from_db(self):
        """Загружает всех живых питомцев из базы данных при старте сервера"""
        pets_data = self.mongo_client.get_all("pets", {"is_alive": True})

        for pet_data in pets_data:
            pet = Pet(pet_data["name"], pet_data["health"])
            pet.state.health = pet_data["health"]
            pet.state.happiness = pet_data["happiness"]
            pet.state.hunger = pet_data["hunger"]
            pet.state.is_alive = pet_data["is_alive"]
            self.pet_manager._pets[pet_data["pet_id"]] = pet
            logger.info(f"Loaded pet from DB: {pet_data['name']} (ID: {pet_data['pet_id']})")

    def reload_pets(self):
        """Перезагружает питомцев из базы данных"""
        self.pet_manager._pets = {}
        self._load_pets_from_db()
        logger.info("Reloaded pets from DB")

    def get_handler(self):
        """Возвращает класс обработчика запросов с доступом к менеджеру питомцев"""
        server = self

        class TamagotchiRequestHandler(BaseHTTPRequestHandler):
            def _set_cors_headers(self):
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

            def _set_headers(self, status_code=200, content_type='application/json'):
                self.send_response(status_code)
                self.send_header('Content-type', content_type)
                self._set_cors_headers()
                self.end_headers()

            def _parse_url(self):
                path = urllib.parse.urlparse(self.path).path
                return [part for part in path.split('/')[1:] if part]

            def _get_pet_id(self, parts):
                if len(parts) >= 3 and parts[2].isdigit():  # Изменено с 2 на 3 из-за user_uuid в пути
                    return int(parts[2])
                return None

            def _read_json_body(self):
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length == 0:
                    return None

                try:
                    body = self.rfile.read(content_length)
                    return json.loads(body.decode('utf-8')) if body else None
                except json.JSONDecodeError as e:
                    logger.warning(f"JSON decode error: {e}")
                    return None

            def _send_response(self, data, status_code=200):
                self._set_headers(status_code)
                if data is not None:
                    self.wfile.write(json.dumps(data).encode('utf-8'))

            def _log_request(self):
                logger.info(f"{self.client_address[0]} - {self.command} {self.path}")

            def _verify_user(self, user_uuid):
                """Проверяет существование пользователя по UUID"""
                user = server.mongo_client.find_by_field("users", {"userGuid": user_uuid})
                return user is not None

            def do_OPTIONS(self):
                """Обработка CORS preflight запросов"""
                self._log_request()
                self._set_headers(204)  # No Content для OPTIONS
                self.end_headers()

            def do_GET(self):
                self._log_request()
                parts = self._parse_url()

                # Проверка авторизации для всех запросов, кроме auth
                if not parts or parts[0] == 'auth':
                    return self._send_response({'error': 'Not found'}, 404)

                # Проверка наличия user_uuid в пути
                if len(parts) < 2:
                    return self._send_response({'error': 'Unauthorized'}, 401)

                user_uuid = parts[0]
                if not self._verify_user(user_uuid):
                    return self._send_response({'error': 'Invalid user'}, 403)

                # Теперь parts[1] - это 'pets'
                if parts[1] != 'pets':
                    return self._send_response({'error': 'Not found'}, 404)

                if len(parts) == 2:
                    # GET /{user_uuid}/pets - список питомцев пользователя
                    pets = [
                        {
                            'id': pid,
                            'name': pet.name,
                            'health': pet.state.health,
                            'happiness': pet.state.happiness,
                            'hunger': pet.state.hunger,
                            'is_alive': pet.state.is_alive
                        }
                        for pid, pet in server.pet_manager.get_alive_pets().items()
                        # Фильтруем питомцев по user_uuid
                        if server.mongo_client.find_by_field("pets", {"pet_id": pid, "user_uuid": user_uuid})
                    ]
                    self._send_response(pets)

                elif len(parts) == 3 and parts[2].isdigit():
                    # GET /{user_uuid}/pets/{id}
                    pet_id = int(parts[2])

                    # Проверяем, принадлежит ли питомец пользователю
                    pet_data = server.mongo_client.find_by_field("pets", {"pet_id": pet_id})
                    if not pet_data or pet_data.get("user_uuid") != user_uuid:
                        return self._send_response({'error': 'Pet not found or not owned by user'}, 404)

                    pet = server.pet_manager.get_pet(pet_id)
                    if not pet:
                        return self._send_response({'error': 'Pet not found'}, 404)

                    self._send_response({
                        'id': pet_id,
                        'name': pet.name,
                        'state': str(pet.state)
                    })
                else:
                    self._send_response({'error': 'Not found'}, 404)

            def do_POST(self):
                self._log_request()
                parts = self._parse_url()

                # Обработка запросов авторизации и регистрации
                if parts and parts[0] == 'auth':
                    data = self._read_json_body() or {}

                    if len(parts) == 2 and parts[1] == 'login':
                        # POST /auth/login
                        if 'username' not in data or 'password' not in data:
                            return self._send_response({'error': 'Username and password required'}, 400)

                        user_uuid = server.auth.authorize(data['username'], data['password'])
                        if user_uuid:
                            return self._send_response({'user_uuid': user_uuid})
                        else:
                            return self._send_response({'error': 'Invalid credentials'}, 401)

                    elif len(parts) == 2 and parts[1] == 'register':
                        # POST /auth/register
                        if 'username' not in data or 'password' not in data:
                            return self._send_response({'error': 'Username and password required'}, 400)

                        if server.auth.registrate(data['username'], data['password']):
                            return self._send_response({'success': True, 'message': 'User registered successfully'})
                        else:
                            return self._send_response({'error': 'Username already exists'}, 400)

                    else:
                        return self._send_response({'error': 'Not found'}, 404)

                # Для всех остальных запросов требуется авторизация
                if not parts or len(parts) < 2:
                    return self._send_response({'error': 'Unauthorized'}, 401)

                user_uuid = parts[0]
                if not self._verify_user(user_uuid):
                    return self._send_response({'error': 'Invalid user'}, 403)

                # Теперь parts[1] - это 'pets'
                if parts[1] != 'pets':
                    return self._send_response({'error': 'Not found'}, 404)

                if len(parts) == 2:
                    # POST /{user_uuid}/pets - создание питомца
                    data = self._read_json_body() or {}

                    if 'name' not in data:
                        return self._send_response({'error': 'Name is required'}, 400)

                    name = data['name']
                    health = data.get('health', 5)

                    if len(name) < 3:
                        return self._send_response({'error': 'Name too short'}, 400)

                    pet_id = server.pet_manager.create_pet(name, health)

                    # Сохраняем питомца в MongoDB с user_uuid
                    server.mongo_client.insert_one("pets", {
                        "pet_id": pet_id,
                        "name": name,
                        "health": health,
                        "happiness": 5,
                        "hunger": 5,
                        "is_alive": True,
                        "created_at": datetime.now().isoformat(),
                        "last_updated": datetime.now().isoformat(),
                        "user_uuid": user_uuid
                    })

                    self._send_response({'id': pet_id}, 201)

                elif len(parts) == 4 and parts[2].isdigit():
                    # POST /{user_uuid}/pets/{id}/{action}
                    actions = {
                        'feed': 'feed',
                        'stroke': 'stroke',
                        'treat': 'give_treat',
                        'walk': 'walk',
                        'ignore': 'ignore'
                    }

                    action = actions.get(parts[3])
                    if not action:
                        return self._send_response({'error': 'Invalid action'}, 400)

                    pet_id = int(parts[2])

                    # Проверяем, принадлежит ли питомец пользователю
                    pet_data = server.mongo_client.find_by_field("pets", {"pet_id": pet_id})
                    if not pet_data or pet_data.get("user_uuid") != user_uuid:
                        return self._send_response({'error': 'Pet not found or not owned by user'}, 404)

                    pet = server.pet_manager.get_pet(pet_id)
                    if not pet:
                        return self._send_response({'error': 'Pet not found'}, 404)

                    if not pet.state.is_alive:
                        return self._send_response({'error': 'Pet is dead'}, 400)

                    # Выполняем действие
                    getattr(pet, action)()

                    # Обновляем состояние в MongoDB
                    server.mongo_client.update_one(
                        "pets",
                        {"pet_id": pet_id},
                        {
                            "health": pet.state.health,
                            "happiness": pet.state.happiness,
                            "hunger": pet.state.hunger,
                            "is_alive": pet.state.is_alive,
                            "last_updated": datetime.now().isoformat()
                        }
                    )

                    self._send_response({
                        'id': pet_id,
                        'action': parts[3],
                        'state': str(pet.state)
                    })
                else:
                    self._send_response({'error': 'Not found'}, 404)

            def do_DELETE(self):
                self._log_request()
                parts = self._parse_url()

                # Проверка авторизации
                if not parts or len(parts) < 3 or parts[1] != 'pets' or not parts[2].isdigit():
                    return self._send_response({'error': 'Not found'}, 404)

                user_uuid = parts[0]
                if not self._verify_user(user_uuid):
                    return self._send_response({'error': 'Invalid user'}, 403)

                pet_id = int(parts[2])

                # Проверяем, принадлежит ли питомец пользователю
                pet_data = server.mongo_client.find_by_field("pets", {"pet_id": pet_id})
                if not pet_data or pet_data.get("user_uuid") != user_uuid:
                    return self._send_response({'error': 'Pet not found or not owned by user'}, 404)

                if server.pet_manager.remove_pet(pet_id):
                    # Помечаем питомца как удалённого в MongoDB
                    server.mongo_client.update_one(
                        "pets",
                        {"pet_id": pet_id},
                        {"is_alive": False, "deleted_at": datetime.now().isoformat()}
                    )
                    self._set_headers(204)
                else:
                    self._send_response({'error': 'Pet not found'}, 404)

        return TamagotchiRequestHandler

if __name__ == '__main__':
        server = TamagotchiServer()
        server.run()