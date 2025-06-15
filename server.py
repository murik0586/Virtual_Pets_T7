from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse
from datetime import datetime
import logging
from entity.Pet import Pet
from entity.PetState import PetState
from entity.PetManager import PetManager
from mongoDBClient.mongoDBClient import MongoDBClient

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

#Инициализация класса взаимодействия с питомцами
pet_manager = PetManager()


class TamagotchiServer:
    def __init__(self):
        self.pet_manager = PetManager()
        self.mongo_client = MongoDBClient(
            uri="mongodb://localhost:27017/",
            db_name="tamagotchi_db",
            username="admin",
            password="12345"
        )
        self._load_pets_from_db()

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

    def get_handler(self):
        """Возвращает класс обработчика запросов с доступом к менеджеру питомцев"""
        server = self

        class TamagotchiRequestHandler(BaseHTTPRequestHandler):
            def _set_cors_headers(self):
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')

            def _set_headers(self, status_code=200, content_type='application/json'):
                self.send_response(status_code)
                self.send_header('Content-type', content_type)
                self._set_cors_headers()
                self.end_headers()

            def _parse_url(self):
                path = urllib.parse.urlparse(self.path).path
                return [part for part in path.split('/')[1:] if part]

            def _get_pet_id(self, parts):
                if len(parts) >= 2 and parts[1].isdigit():
                    return int(parts[1])
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

            def do_OPTIONS(self):
                """Обработка CORS preflight запросов"""
                self._log_request()
                self._set_headers(204)  # No Content для OPTIONS
                self.end_headers()

            def do_GET(self):
                self._log_request()
                parts = self._parse_url()

                if not parts or parts[0] != 'pets':
                    return self._send_response({'error': 'Not found'}, 404)

                if len(parts) == 1:
                    # GET /pets - список питомцев
                    pets = [
                        {
                            'id': pid,
                            'name': pet.name,
                            'health': pet.state.health,
                            'happiness': pet.state.happiness,
                            'hunger': pet.state.hunger,
                            'is_alive': pet.state.is_alive
                        }
                        for pid, pet in pet_manager.get_alive_pets().items()
                    ]
                    self._send_response(pets)

                elif len(parts) == 2 and parts[1].isdigit():
                    # GET /pets/{id}
                    pet = pet_manager.get_pet(int(parts[1]))
                    if not pet:
                        return self._send_response({'error': 'Pet not found'}, 404)

                    self._send_response({
                        'id': int(parts[1]),
                        'name': pet.name,
                        'state': str(pet.state)
                    })
                else:
                    self._send_response({'error': 'Not found'}, 404)

                    def do_POST(self):
                        self._log_request()
                        parts = self._parse_url()

                        if not parts or parts[0] != 'pets':
                            return self._send_response({'error': 'Not found'}, 404)

                        if len(parts) == 1:
                            # POST /pets - создание питомца
                            data = self._read_json_body() or {}

                            if 'name' not in data:
                                return self._send_response({'error': 'Name is required'}, 400)

                            name = data['name']
                            health = data.get('health', 5)

                            if len(name) < 3:
                                return self._send_response({'error': 'Name too short'}, 400)

                            pet_id = server.pet_manager.create_pet(name, health)

                            # Сохраняем питомца в MongoDB
                            server.mongo_client.insert_one("pets", {
                                "pet_id": pet_id,
                                "name": name,
                                "health": health,
                                "happiness": 5,
                                "hunger": 5,
                                "is_alive": True,
                                "created_at": datetime.now().isoformat(),
                                "last_updated": datetime.now().isoformat()
                            })

                            self._send_response({'id': pet_id}, 201)

                        elif len(parts) == 3 and parts[1].isdigit():
                            # POST /pets/{id}/{action}
                            actions = {
                                'feed': 'feed',
                                'stroke': 'stroke',
                                'treat': 'give_treat',
                                'walk': 'walk',
                                'ignore': 'ignore'
                            }

                            action = actions.get(parts[2])
                            if not action:
                                return self._send_response({'error': 'Invalid action'}, 400)

                            pet_id = int(parts[1])
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
                                'action': parts[2],
                                'state': str(pet.state)
                            })
                        else:
                            self._send_response({'error': 'Not found'}, 404)

                    def do_DELETE(self):
                        self._log_request()
                        parts = self._parse_url()

                        if not parts or parts[0] != 'pets' or len(parts) != 2 or not parts[1].isdigit():
                            return self._send_response({'error': 'Not found'}, 404)

                        pet_id = int(parts[1])
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

    def run(self, port=8000):
        server_address = ('', port)
        httpd = HTTPServer(server_address, self.get_handler())
        logger.info(f"Starting server on port {port}")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info("Server stopped")
        finally:
            self.mongo_client.close()
            httpd.server_close()

if __name__ == '__main__':
        server = TamagotchiServer()
        server.run()