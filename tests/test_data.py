from app import create_app
from app.models import CrowdData
from datetime import datetime, timedelta
import random

def generate_test_data():
    app = create_app()
    with app.app_context():
        # Clear existing data
        CrowdData.objects.delete()
        
        # Generate 200 test records
        for i in range(200):
            CrowdData(
                device_id=f"pi_{random.randint(1, 3)}",
                people_count=random.randint(0, 30),
                detections=[
                    [random.randint(0,300), random.randint(0,300),
                    random.randint(300,600), random.randint(300,600)]
                    for _ in range(random.randint(1, 5))
                ],
                timestamp=datetime.utcnow() - timedelta(minutes=random.randint(0, 1440)),
                is_anomaly=random.random() > 0.85
            ).save()
        print("Generated 200 test records")

if __name__ == '__main__':
    generate_test_data()