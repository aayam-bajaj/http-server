from datetime import datetime
from pymongo import IndexModel, ASCENDING, DESCENDING

class CrowdData:
    def __init__(self, db):
        self.collection = db['crowd_data']
        self.analytics_collection = db['analytics'] 
        self._create_indexes()
    
    def _create_indexes(self):
        indexes = [
            IndexModel([('timestamp', DESCENDING)]),
            IndexModel([('device_id', ASCENDING)]),
            IndexModel([('location', ASCENDING)])]
        self.collection.create_indexes(indexes)

     # NEW analytics indexes
        analytics_indexes = [
            IndexModel([('timestamp', DESCENDING)]),
            IndexModel([('edge_data.device_id', ASCENDING)]),
            IndexModel([('anomalies', ASCENDING)])
        ]
        self.analytics_collection.create_indexes(analytics_indexes)
    
    def insert_data(self, data):
        """Insert crowd data with timestamp"""
        data['timestamp'] = datetime.now()
        return self.collection.insert_one(data)
    
    def get_recent_data(self, limit=100):
        """Get most recent crowd data"""
        return list(self.collection.find().sort('timestamp', -1).limit(limit))
    
    def get_stats(self):
        """Calculate statistics"""
        pipeline = [
            {'$group': {
                '_id': None,
                'total_people': {'$sum': '$count'},
                'avg_density': {'$avg': '$density'},
                'active_locations': {'$addToSet': '$location'}
            }}
        ]
        result = list(self.collection.aggregate(pipeline))
        if result:
            stats = result[0]
            stats['active_locations'] = len(stats['active_locations'])
            return stats
        return {
            'total_people': 0,
            'avg_density': 0,
            'active_locations': 0
        }
    
    # NEW method for advanced analytics
    def insert_analytics(self, data):
        """Insert YOLO/DeepSort processed data"""
        data['processed_at'] = datetime.now()
        return self.analytics_collection.insert_one(data)