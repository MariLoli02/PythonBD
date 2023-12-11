import json
import pytest
from flask import Flask
from app.models import Data
from app import db
from app.routes import data_routes 

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(data_routes)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.init_app(app)
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_insert_data(client):
    data = {"name": "TestName"}
    response = client.post('/data', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Data inserted successfully"}

def test_insert_duplicate_data(client):
    data = {"name": "TestName"}
    # Insert data for the first time
    response = client.post('/data', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200

    # Try to insert the same data again
    response = client.post('/data', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 409
    assert response.get_json() == {"message": "Data already exists"}

def test_get_all_data(client):
    # Insert some test data
    test_data = [{"name": "TestName1"}, {"name": "TestName2"}]
    for data in test_data:
        client.post('/data', data=json.dumps(data), content_type='application/json')

    # Retrieve all data
    response = client.get('/data')
    assert response.status_code == 200
    assert response.get_json() == [{"id": 1, "name": "TestName1"}, {"id": 2, "name": "TestName2"}]

def test_delete_data(client):
    # Insert test data
    data = {"name": "TestName"}
    response = client.post('/data', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200

    # Delete the inserted data
    response = client.delete('/data/1')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Data deleted successfully"}

def test_delete_nonexistent_data(client):
    # Attempt to delete data that does not exist
    response = client.delete('/data/1')
    assert response.status_code == 404
    assert response.get_json() == {"message": "Data not found"}
                                   
