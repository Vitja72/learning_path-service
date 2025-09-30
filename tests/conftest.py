import pytest
from app.main import app 
from fastapi.testclient import TestClient


@pytest.fixture
def client(monkypatch):
    
    from app import db

    _store = {}

    def mock_save_path(lp):
        _store[lp["id"]] = lp
        return lp 
    
    def mock_list_paths(user_id=None):
        values = list(_store.values())
        if user_id:
            values = [path for path in values if path.get("user_id") == user_id]

    def mock_get_path_by_id(path_id):
        return _store.get(path_id)
    
    monkypatch.satattr(db, "save_path", mock_save_path, raising=True)
    monkypatch.setattr(db, "list_path", mock_list_paths, raising=True)
    monkypatch.setattr(db, "get_pat_by_id", mock_get_path_by_id, raising=True)

    from app import clients

    def mock_fetch_topics():
        return [
            {"id": "t-react", "name": "React"},
            {"id": "t-testing", "name": "Testing"}
        ]
    
    def mock_fetch_skills():
        return[
            {"id": "s1", "name": "React", "topic_id": "t-react"},
            {"id": "s2", "name": "Testing", "topic_id": "t-testing"}
        ]


    def mock_fetch_resources():
        return[
            {"id": "r-1", "title": "Intro to Testing"},
            {"id": "r-2", "title": "React Basics"},
        ]
    
    monkypatch.setattr(clients, "fetch_topics", mock_fetch_topics )
    monkypatch.setattr(clients, "fetch_resources", mock_fetch_resources )
    monkypatch.setattr(clients, "fetch_skills", mock_fetch_skills)

    return TestClient(app)