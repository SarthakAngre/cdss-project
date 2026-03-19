import uuid
from typing import Optional

class SessionStore:
    _store: dict = {}

    @classmethod
    def create(cls, username: str) -> str:
        session_id = str(uuid.uuid4())
        cls._store[session_id] = {"username": username}
        return session_id

    @classmethod
    def get(cls, session_id: str) -> Optional[dict]:
        return cls._store.get(session_id)

    @classmethod
    def delete(cls, session_id: str):
        cls._store.pop(session_id, None)