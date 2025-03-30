from mongoengine import connect, Document, StringField, IntField, ListField, DateTimeField, BooleanField
from datetime import datetime
from config import Config

# Simple local connection
connect(host=Config.MONGO_URI)

class CrowdData(Document):
    device_id = StringField(required=True, default="raspberry_pi")
    people_count = IntField(required=True)
    detections = ListField(ListField(IntField()))  # [[x1,y1,x2,y2], ...]
    timestamp = DateTimeField(default=datetime.now)  # Local time
    is_anomaly = BooleanField(default=False)
    
    meta = {
        'collection': 'crowd_events',  # Explicit collection name
        'indexes': [
            '-timestamp'  # Single descending index
        ]
    }