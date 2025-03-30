from app import db
from datetime import datetime

class CrowdData(db.Document):
    device_id = db.StringField(required=True)
    people_count = db.IntField(required=True)
    detections = db.ListField(db.ListField(db.IntField()))
    timestamp = db.DateTimeField(default=datetime.utcnow)
    is_anomaly = db.BooleanField(default=False)
    
    meta = {
        'collection': 'crowd_events',
        'indexes': [
            '-timestamp',
            'device_id'
        ]
    }