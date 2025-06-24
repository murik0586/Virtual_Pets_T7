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

    # Добавляем мок для find_by_field, чтобы проверять пользователя
    def mock_find_by_field(collection_name, query):
        if collection_name == "users" and "userGuid" in query:
            if query["userGuid"] == "test-user-uuid":
                return {"username": "testuser", "userGuid": "test-user-uuid"}
        elif collection_name == "pets":
            pet_id = query.get("pet_id")
            if pet_id in [1, 2]:
                return {"pet_id": pet_id, "name": f"Pet{pet_id}", "user_uuid": "test-user-uuid"}
        return None

    mock_client.find_by_field.side_effect = mock_find_by_field

    # Добавляем мок для find_user
    def mock_find_user(collection_name, username):
        if username == "testuser":
            return {"username": "testuser", "password": "hashed_password", "userGuid": "test-user-uuid"}
        return None

    mock_client.find_user.side_effect = mock_find_user

    return mock_client


@pytest.fixture
def mock_auth():
    mock_auth = MagicMock()

    def mock_authorize(username, password):
        if username == "testuser" and password == "password":
            return "test-user-uuid"
        return None

    def mock_registrate(username, password):
        if username == "newuser":
            return True
        return False

    mock_auth.authorize.side_effect = mock_authorize
    mock_auth.registrate.side_effect = mock_registrate

    return mock_auth


@pytest.fixture
def tamagotchi_server(mock_mongodb_client, mock_auth):
    from server import TamagotchiServer

    # Передаем мок в конструктор
    server = TamagotchiServer(mongo_client=mock_mongodb_client)

    # Заменяем объект авторизации на мок
    server.auth = mock_auth

    server.run(port=0, block=False)
    server_url = f"http://localhost:{server.port}"

    yield server, server_url

    server.httpd.shutdown()
    server.thread.join()


class TestTamagotchiServer:
    def test_register_user(self, tamagotchi_server, mock_auth):
        server, server_url = tamagotchi_server

        # Регистрация нового пользователя
        response = requests.post(
            f"{server_url}/auth/register",
            json={"username": "newuser", "password": "password123"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

        # Проверка вызова метода регистрации
        mock_auth.registrate.assert_called_once_with("newuser", "password123")

    def test_register_existing_user(self, tamagotchi_server, mock_auth):
        server, server_url = tamagotchi_server

        # Попытка регистрации существующего пользователя
        response = requests.post(
            f"{server_url}/auth/register",
            json={"username": "testuser", "password": "password"}
        )

        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    def test_login_user(self, tamagotchi_server, mock_auth):
        server, server_url = tamagotchi_server

        # Авторизация пользователя
        response = requests.post(
            f"{server_url}/auth/login",
            json={"username": "testuser", "password": "password"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["user_uuid"] == "test-user-uuid"

        # Проверка вызова метода авторизации
        mock_auth.authorize.assert_called_once_with("testuser", "password")

    def test_login_invalid_credentials(self, tamagotchi_server, mock_auth):
        server, server_url = tamagotchi_server

        # Попытка авторизации с неверными данными
        response = requests.post(
            f"{server_url}/auth/login",
            json={"username": "testuser", "password": "wrong_password"}
        )

        assert response.status_code == 401
        data = response.json()
        assert "error" in data

    def test_create_pet(self, tamagotchi_server, mock_mongodb_client):
        server, server_url = tamagotchi_server
        response = requests.post(
            f"{server_url}/test-user-uuid/pets",
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
        assert document["user_uuid"] == "test-user-uuid"  # Проверка user_uuid

    def test_get_all_pets(self, tamagotchi_server, mock_mongodb_client):
        server, server_url = tamagotchi_server

        # Настройка моков
        pets_data = [
            {"pet_id": 1, "name": "Rex", "health": 7, "happiness": 6, "hunger": 3, "is_alive": True,
             "user_uuid": "test-user-uuid"},
            {"pet_id": 2, "name": "Whiskers", "health": 5, "happiness": 8, "hunger": 4, "is_alive": True,
             "user_uuid": "test-user-uuid"}
        ]
        mock_mongodb_client.get_all.return_value = pets_data

        # Принудительная перезагрузка
        server.reload_pets()

        # Проверка API
        response = requests.get(f"{server_url}/test-user-uuid/pets")
        assert response.status_code == 200
        pets = response.json()
        assert len(pets) == 2
        names = {pet['name'] for pet in pets}
        assert names == {"Rex", "Whiskers"}

    def test_get_single_pet(self, tamagotchi_server, mock_mongodb_client):
        server, server_url = tamagotchi_server
        response = requests.post(
            f"{server_url}/test-user-uuid/pets",
            json={"name": "Spot"}
        )
        pet_id = response.json()['id']

        response = requests.get(f"{server_url}/test-user-uuid/pets/{pet_id}")
        assert response.status_code == 200

        pet = response.json()
        assert pet['id'] == pet_id
        assert pet['name'] == "Spot"
        assert 'state' in pet

    def test_feed_pet(self, tamagotchi_server, mock_mongodb_client):
        server, server_url = tamagotchi_server

        # Создаем питомца
        response = requests.post(
            f"{server_url}/test-user-uuid/pets",
            json={"name": "Buddy"}
        )
        pet_id = response.json()['id']

        # Сбрасываем счетчик
        mock_mongodb_client.update_one.reset_mock()

        # Кормим питомца
        response = requests.post(f"{server_url}/test-user-uuid/pets/{pet_id}/feed")
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
            f"{server_url}/test-user-uuid/pets",
            json={"name": "Milo"}
        )
        pet_id = response.json()['id']

        response = requests.post(f"{server_url}/test-user-uuid/pets/{pet_id}/fly")
        assert response.status_code == 400
        assert response.json()['error'] == 'Invalid action'

    def test_delete_pet(self, tamagotchi_server, mock_mongodb_client):
        server, server_url = tamagotchi_server

        # Создаем питомца
        response = requests.post(
            f"{server_url}/test-user-uuid/pets",
            json={"name": "Charlie"}
        )
        pet_id = response.json()['id']

        # Сбрасываем счетчик
        mock_mongodb_client.update_one.reset_mock()

        # Удаляем питомца
        response = requests.delete(f"{server_url}/test-user-uuid/pets/{pet_id}")
        assert response.status_code == 204

        # Проверяем вызов БД
        mock_mongodb_client.update_one.assert_called_once()
        call_args = mock_mongodb_client.update_one.call_args[0]
        assert call_args[0] == "pets"
        assert call_args[1] == {"pet_id": pet_id}
        assert call_args[2]["is_alive"] is False

    def test_cors_headers(self, tamagotchi_server):
        server, server_url = tamagotchi_server
        response = requests.options(server_url + "/test-user-uuid/pets")
        assert response.status_code == 204
        assert response.headers['Access-Control-Allow-Origin'] == '*'
        assert response.headers['Access-Control-Allow-Methods'] == 'GET, POST, DELETE, OPTIONS'
        assert 'Content-Type' in response.headers['Access-Control-Allow-Headers']
        assert 'Authorization' in response.headers['Access-Control-Allow-Headers']

    def test_validation_errors(self, tamagotchi_server):
        server, server_url = tamagotchi_server
        response = requests.post(
            f"{server_url}/test-user-uuid/pets",
            json={"name": "A"}
        )
        assert response.status_code == 400
        assert response.json()['error'] == 'Name too short'

        response = requests.post(
            f"{server_url}/test-user-uuid/pets",
            json={}
        )
        assert response.status_code == 400
        assert response.json()['error'] == 'Name is required'

    def test_pet_not_found(self, tamagotchi_server):
        server, server_url = tamagotchi_server
        response = requests.get(f"{server_url}/test-user-uuid/pets/999")
        assert response.status_code == 404
        assert response.json()['error'] == 'Pet not found or not owned by user'

        response = requests.post(f"{server_url}/test-user-uuid/pets/999/feed")
        assert response.status_code == 404
        assert response.json()['error'] == 'Pet not found or not owned by user'

        response = requests.delete(f"{server_url}/test-user-uuid/pets/999")
        assert response.status_code == 404
        assert response.json()['error'] == 'Pet not found or not owned by user'

    def test_dead_pet_action(self, tamagotchi_server, mock_mongodb_client):
        server, server_url = tamagotchi_server

        # Настройка моков для мертвого питомца
        mock_mongodb_client.get_all.return_value = [
            {"pet_id": 1, "name": "Ghost", "health": 0, "happiness": 0, "hunger": 10, "is_alive": False,
             "user_uuid": "test-user-uuid"}
        ]

        # Принудительная перезагрузка
        server.reload_pets()

        # Проверяем API
        response = requests.post(f"{server_url}/test-user-uuid/pets/1/feed")
        assert response.status_code == 400
        assert response.json()['error'] == 'Pet is dead'

    def test_unauthorized_access(self, tamagotchi_server):
        server, server_url = tamagotchi_server

        # Попытка доступа без user_uuid
        response = requests.get(f"{server_url}/pets")
        assert response.status_code == 401

        # Попытка доступа с неверным user_uuid
        response = requests.get(f"{server_url}/invalid-uuid/pets")
        assert response.status_code == 403

    def test_access_other_user_pet(self, tamagotchi_server, mock_mongodb_client):
        server, server_url = tamagotchi_server

        # Создаем питомца для тестового пользователя
        response = requests.post(
            f"{server_url}/test-user-uuid/pets",
            json={"name": "OwnedPet"}
        )
        pet_id = response.json()['id']

        # Модифицируем мок для имитации доступа к чужому питомцу
        def mock_find_by_field_other_user(collection_name, query):
            if collection_name == "users":
                if query.get("userGuid") == "other-user-uuid":
                    return {"username": "otheruser", "userGuid": "other-user-uuid"}
                elif query.get("userGuid") == "test-user-uuid":
                    return {"username": "testuser", "userGuid": "test-user-uuid"}
            elif collection_name == "pets" and query.get("pet_id") == pet_id:
                return {"pet_id": pet_id, "name": "OwnedPet", "user_uuid": "test-user-uuid"}
            return None

        mock_mongodb_client.find_by_field.side_effect = mock_find_by_field_other_user

        # Попытка доступа к питомцу другого пользователя
        response = requests.get(f"{server_url}/other-user-uuid/pets/{pet_id}")
        assert response.status_code == 404
        assert response.json()['error'] == 'Pet not found or not owned by user'