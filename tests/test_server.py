import pytest
import requests
import json
from unittest.mock import MagicMock, patch, call
from http.server import BaseHTTPRequestHandler
from datetime import datetime

# Фикстура для мокирования MongoDBClient
@pytest.fixture
def mock_mongodb_client():
    mock_client = MagicMock()
    mock_client.get_all.return_value = []
    return mock_client

@pytest.fixture
def tamagotchi_server(mock_mongodb_client):
    from server import TamagotchiServer

    # Передаем мок в конструктор
    server = TamagotchiServer(mongo_client=mock_mongodb_client)
    server.run(port=0, block=False)
    server_url = f"http://localhost:{server.port}"

    yield server, server_url

    server.httpd.shutdown()
    server.thread.join()


class TestTamagotchiServer:
    def test_create_pet(self, tamagotchi_server, mock_mongodb_client):
        server, server_url = tamagotchi_server
        response = requests.post(
            f"{server_url}/pets",
            json={"name": "Fluffy", "health": 8}
        )

        assert response.status_code == 201
        data = response.json()
        assert 'id' in data
        pet_id = data['id']

        # Проверка вызова MongoDB
        mock_mongodb_client.insert_one.assert_called_once()
        call_args = mock_mongodb_client.insert_one.call_args[0]
        assert call_args[0] == "pets"
        document = call_args[1]
        assert document["name"] == "Fluffy"
        assert document["health"] == 8
        assert document["pet_id"] == pet_id
        assert document["is_alive"] is True

    def test_get_all_pets(self, tamagotchi_server, mock_mongodb_client):
        server, server_url = tamagotchi_server

        # Настройка моков
        pets_data = [
            {"pet_id": 1, "name": "Rex", "health": 7, "happiness": 6, "hunger": 3, "is_alive": True},
            {"pet_id": 2, "name": "Whiskers", "health": 5, "happiness": 8, "hunger": 4, "is_alive": True}
        ]
        mock_mongodb_client.get_all.return_value = pets_data

        # Принудительная перезагрузка
        server.reload_pets()

        # Проверка API
        response = requests.get(f"{server_url}/pets")
        assert response.status_code == 200
        pets = response.json()
        assert len(pets) == 2
        names = {pet['name'] for pet in pets}
        assert names == {"Rex", "Whiskers"}

    def test_get_single_pet(self, tamagotchi_server, mock_mongodb_client):
        server, server_url = tamagotchi_server
        response = requests.post(
            f"{server_url}/pets",
            json={"name": "Spot"}
        )
        pet_id = response.json()['id']

        response = requests.get(f"{server_url}/pets/{pet_id}")
        assert response.status_code == 200

        pet = response.json()
        assert pet['id'] == pet_id
        assert pet['name'] == "Spot"
        assert 'state' in pet

    def test_feed_pet(self, tamagotchi_server, mock_mongodb_client):
        server, server_url = tamagotchi_server

        # Создаем питомца
        response = requests.post(
            f"{server_url}/pets",
            json={"name": "Buddy"}
        )
        pet_id = response.json()['id']

        # Сбрасываем счетчик
        mock_mongodb_client.update_one.reset_mock()

        # Кормим питомца
        response = requests.post(f"{server_url}/pets/{pet_id}/feed")
        assert response.status_code == 200

        # Проверяем вызов БД
        mock_mongodb_client.update_one.assert_called_once()
        call_args = mock_mongodb_client.update_one.call_args[0]
        assert call_args[0] == "pets"
        assert call_args[1] == {"pet_id": pet_id}
        assert "hunger" in call_args[2]

    def test_invalid_action(self, tamagotchi_server):
        server, server_url = tamagotchi_server
        response = requests.post(
            f"{server_url}/pets",
            json={"name": "Milo"}
        )
        pet_id = response.json()['id']

        response = requests.post(f"{server_url}/pets/{pet_id}/fly")
        assert response.status_code == 400
        assert response.json()['error'] == 'Invalid action'

    def test_delete_pet(self, tamagotchi_server, mock_mongodb_client):
        server, server_url = tamagotchi_server

        # Создаем питомца
        response = requests.post(
            f"{server_url}/pets",
            json={"name": "Charlie"}
        )
        pet_id = response.json()['id']

        # Сбрасываем счетчик
        mock_mongodb_client.update_one.reset_mock()

        # Удаляем питомца
        response = requests.delete(f"{server_url}/pets/{pet_id}")
        assert response.status_code == 204

        # Проверяем вызов БД
        mock_mongodb_client.update_one.assert_called_once()
        call_args = mock_mongodb_client.update_one.call_args[0]
        assert call_args[0] == "pets"
        assert call_args[1] == {"pet_id": pet_id}
        assert call_args[2]["is_alive"] is False

    def test_cors_headers(self, tamagotchi_server):
        server, server_url = tamagotchi_server
        response = requests.options(server_url + "/pets")
        assert response.status_code == 204
        assert response.headers['Access-Control-Allow-Origin'] == '*'
        assert response.headers['Access-Control-Allow-Methods'] == 'GET, POST, DELETE, OPTIONS'
        assert response.headers['Access-Control-Allow-Headers'] == 'Content-Type'

    def test_validation_errors(self, tamagotchi_server):
        server, server_url = tamagotchi_server
        response = requests.post(
            f"{server_url}/pets",
            json={"name": "A"}
        )
        assert response.status_code == 400
        assert response.json()['error'] == 'Name too short'

        response = requests.post(
            f"{server_url}/pets",
            json={}
        )
        assert response.status_code == 400
        assert response.json()['error'] == 'Name is required'

    def test_pet_not_found(self, tamagotchi_server):
        server, server_url = tamagotchi_server
        response = requests.get(f"{server_url}/pets/999")
        assert response.status_code == 404
        assert response.json()['error'] == 'Pet not found'

        response = requests.post(f"{server_url}/pets/999/feed")
        assert response.status_code == 404
        assert response.json()['error'] == 'Pet not found'

        response = requests.delete(f"{server_url}/pets/999")
        assert response.status_code == 404
        assert response.json()['error'] == 'Pet not found'

    def test_dead_pet_action(self, tamagotchi_server, mock_mongodb_client):
        server, server_url = tamagotchi_server

        # Настройка моков для мертвого питомца
        mock_mongodb_client.get_all.return_value = [
            {"pet_id": 1, "name": "Ghost", "health": 0, "happiness": 0, "hunger": 10, "is_alive": False}
        ]

        # Принудительная перезагрузка
        server.reload_pets()

        # Проверяем API
        response = requests.post(f"{server_url}/pets/1/feed")
        assert response.status_code == 400
        assert response.json()['error'] == 'Pet is dead'