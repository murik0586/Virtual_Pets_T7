from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse
from datetime import datetime
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Импорт ваших классов (должны быть в тех же файлах)
from entity.Pet import Pet
from entity.PetState import PetState
from entity.PetManager import PetManager

pet_manager = PetManager()


class TamagotchiRequestHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _set_headers(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self._set_cors_headers()  # CORS-заголовки
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

            pet_id = pet_manager.create_pet(name, health)
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

            pet = pet_manager.get_pet(int(parts[1]))
            if not pet:
                return self._send_response({'error': 'Pet not found'}, 404)

            if not pet.state.is_alive:
                return self._send_response({'error': 'Pet is dead'}, 400)

            getattr(pet, action)()
            self._send_response({
                'id': int(parts[1]),
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

        if pet_manager.remove_pet(int(parts[1])):
            self._set_headers(204)
        else:
            self._send_response({'error': 'Pet not found'}, 404)


def run(server_class=HTTPServer, handler_class=TamagotchiRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logger.info(f"Starting server on port {port}")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped")
    finally:
        httpd.server_close()


if __name__ == '__main__':
    run()