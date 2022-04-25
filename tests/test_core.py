import pytest
from sales.db import get_db


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"BigMamma sales" in response.data


def test_reload_data(client):
    response = client.get('/reload')
    assert response.status_code == 200
    assert b"BigMamma sales" in response.data

