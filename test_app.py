import os
import tempfile
import pytest
import app as app_module

@pytest.fixture
def client():
    db_fd, app_module.DB_PATH = tempfile.mkstemp()
    app_module.app.config['TESTING'] = True
    with app_module.app.test_client() as client:
        yield client
    os.close(db_fd)
    os.unlink(app_module.DB_PATH)

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
