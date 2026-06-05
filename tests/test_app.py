import pytest

from app.main import app as flask_app


@pytest.fixture
def client():
    flask_app.config.update({"TESTING": True})
    with flask_app.test_client() as client:
        yield client


def test_index(client):
    r = client.get('/')
    assert r.status_code == 200
    assert b'Minimal Flask App' in r.data


def test_echo_default(client):
    r = client.get('/api/echo')
    assert r.status_code == 200
    assert r.is_json
    assert r.get_json().get('echo') == 'hello'


def test_echo_with_msg(client):
    r = client.get('/api/echo?msg=testing')
    assert r.status_code == 200
    assert r.get_json().get('echo') == 'testing'
