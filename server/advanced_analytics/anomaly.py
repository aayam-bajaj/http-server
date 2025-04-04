from collections import defaultdict

class AnomalyDetector:
    def __init__(self, crowd_threshold=5, dwell_threshold=60):
        self.crowd_threshold = crowd_threshold
        self.dwell_threshold = dwell_threshold
        self.track_history = defaultdict(list)
    
    def detect(self, tracks):
        anomalies = []
        
        # Crowding detection
        if len(tracks) > self.crowd_threshold:
            anomalies.append("crowding")
        
        # Loitering detection
        for track in tracks:
            if track["dwell_time"] > self.dwell_threshold:
                anomalies.append(f"loitering_{track['id']}")
                
        return anomalies