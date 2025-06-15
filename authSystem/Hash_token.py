import hashlib
import uuid

class Hash_token:

    def hash_password(self, password: str) -> str:
        hash_object = hashlib.sha256()
        hash_object.update(password.encode('utf-8'))  # Преобразуем строку в байты.
        return hash_object.hexdigest()  # Возвращаем хэш.

    def generate_guid(self) -> str:
        return str(uuid.uuid4())