import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import pytest
import hashlib
import uuid
from authSystem.Hash_token import Hash_token

@pytest.fixture
def hash_token():
    return Hash_token()

# Тесты для hash_password
def test_hash_password_returns_correct_sha256_hash(hash_token):
    """Проверка корректности вычисления SHA-256 хэша"""
    password = "secure_password"
    expected_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    assert hash_token.hash_password(password) == expected_hash

def test_hash_password_same_input_same_output(hash_token):
    """Одинаковые пароли должны давать одинаковый хэш"""
    assert hash_token.hash_password("12345") == hash_token.hash_password("12345")

def test_hash_password_different_inputs_different_outputs(hash_token):
    """Разные пароли должны давать разные хэши"""
    assert hash_token.hash_password("password1") != hash_token.hash_password("password2")

def test_hash_password_empty_string(hash_token):
    """Проверка обработки пустой строки"""
    empty_hash = hashlib.sha256().hexdigest()
    assert hash_token.hash_password("") == empty_hash

def test_hash_password_format(hash_token):
    """Проверка формата выходных данных (64 hex-символа)"""
    result = hash_token.hash_password("test")
    assert len(result) == 64
    assert all(c in "0123456789abcdef" for c in result)

# Тесты для generate_guid
def test_generate_guid_returns_string(hash_token):
    """Проверка типа возвращаемого значения"""
    assert isinstance(hash_token.generate_guid(), str)

def test_generate_guid_valid_uuid4_format(hash_token):
    """Проверка соответствия формату UUIDv4"""
    guid = hash_token.generate_guid()
    parsed_uuid = uuid.UUID(guid, version=4)
    assert str(parsed_uuid) == guid

def test_generate_guid_uniqueness(hash_token):
    """Проверка уникальности GUID"""
    guids = {hash_token.generate_guid() for _ in range(100)}
    assert len(guids) == 100

def test_generate_guid_version_and_variant(hash_token):
    """Проверка версии и варианта UUID"""
    guid = uuid.UUID(hash_token.generate_guid())
    assert guid.version == 4
    assert guid.variant == uuid.RFC_4122