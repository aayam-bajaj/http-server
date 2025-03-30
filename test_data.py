from models import CrowdData
from datetime import datetime, timedelta
import random

def generate_test_data():
    # Clear old test data
    CrowdData.objects.delete()
    
    # Generate realistic test data matching edge device format
    for i in range(200):
        CrowdData(
            device_id="test_pi",
            people_count=random.randint(0, 25),
            detections=[[random.randint(0,300), random.randint(0,300), 
                       random.randint(300,600), random.randint(300,600)] 
                      for _ in range(random.randint(0, 5))],
            timestamp=datetime.utcnow() - timedelta(minutes=random.randint(0, 1440)),
            is_anomaly=random.random() > 0.8
        ).save()
    print("Generated 200 test records")

if __name__ == '__main__':
    from app import app
    with app.app_context():
        generate_test_data()