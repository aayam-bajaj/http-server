import pytest
from app import app
from models import CrowdData
import zlib
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Setup test database
            app.db = {'crowd_data': {}}
            yield client

def test_receive_data(client):
    # Test data
    test_data = {
        "count": 15,
        "location": "Test Location",
        "area": 10,
        "timestamp": "2023-01-01T00:00:00"
    }
    
    # Compress the data
    compressed = zlib.compress(json.dumps(test_data).encode())
    
    # Send to endpoint
    response = client.post(
        '/api/receive_data',
        data=compressed,
        headers={
            "Content-Type": "application/json",
            "Content-Encoding": "gzip"
        }
    )
    
    assert response.status_code == 200
    assert 'inserted_id' in response.json

def test_get_events(client):
    # First insert some test data
    crowd_data = CrowdData(app.db)
    for i in range(5):
        crowd_data.insert_data({
            "count": i + 10,
            "location": f"Location {i}",
            "area": 10,
            "timestamp": f"2023-01-01T00:00:{i:02d}"
        })
    
    # Test getting events
    response = client.get('/api/events?hours=24&limit=5')
    assert response.status_code == 200
    assert len(response.json) == 5

def test_get_stats(client):
    # Insert test data
    crowd_data = CrowdData(app.db)
    crowd_data.insert_data({
        "count": 10,
        "location": "Location A",
        "area": 10,
        "timestamp": "2023-01-01T00:00:00"
    })
    crowd_data.insert_data({
        "count": 20,
        "location": "Location B",
        "area": 20,
        "timestamp": "2023-01-01T00:01:00"
    })
    
    # Test getting stats
    response = client.get('/api/stats')
    assert response.status_code == 200
    assert response.json['total_people'] == 30
    assert response.json['active_locations'] == 2