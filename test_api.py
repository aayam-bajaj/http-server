import pytest
from app import app
from models import CrowdData
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            CrowdData.objects.delete()  # Clean DB before tests
        yield client

def test_receive_data(client):
    # Test valid data submission
    test_data = {
        "count": 5,
        "detections": [[10,20,30,40]],
        "device": "test_pi"
    }
    response = client.post(
        '/receive_data',
        data=json.dumps(test_data),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert CrowdData.objects.count() == 1

def test_get_data(client):
    # First insert test data
    CrowdData(
        device_id="test_pi",
        people_count=10,
        detections=[[100,100,200,200]]
    ).save()
    
    # Test data retrieval
    response = client.get('/get_data')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['count'] == 10