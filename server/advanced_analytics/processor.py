# from turtle import tracer
# import cv2
# import numpy as np
# import base64
# from datetime import datetime
# from . import yolo, deepsort, heatmap, anomaly

# def process_advanced_analytics(data):
#     """Full processing pipeline for frames"""
#     # Decode frame
#     img_bytes = base64.b64decode(data["full_frame"])
#     frame = cv2.imdecode(np.frombuffer(img_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
    
#     # YOLO Detection
#     results = yolo(frame, classes=0, conf=0.5)  # Only people, 50% confidence
#     detections = [
#         ([x1, y1, x2-x1, y2-y1], conf, 'person')
#         for box in results[0].boxes
#         for x1, y1, x2, y2, conf in [box.xyxy[0].tolist() + [box.conf[0].item()]]]
    
#     # DeepSort Tracking
#     # Replace DeepSort with ByteTrack
#     tracks = tracer.update(
#     detections=np.array([d[0] for d in detections]),  # [x,y,w,h]
#     scores=np.array([d[1] for d in detections])       # confidence
# )
    
#     # Analytics
#     track_data = [{
#         "id": int(t.track_id),
#         "bbox": t.to_ltrb(),
#         "dwell_time": (datetime.now() - t.detection_time).total_seconds()
#     } for t in tracks]
    
#     return {
#         "timestamp": data["timestamp"],
#         "edge_data": {k:v for k,v in data.items() if k != "full_frame"},
#         "yolo_count": len(tracks),
#         "tracks": track_data,
#         "heatmap": heatmap.generate(frame, tracks),
#         "anomalies": anomaly.detect(track_data)
#     }

import cv2
import numpy as np
import base64
from . import yolo

def process_advanced_analytics(data):
    """Simplified YOLO-only processing"""
    try:
        # Decode frame
        img_bytes = base64.b64decode(data["full_frame"])
        frame = cv2.imdecode(np.frombuffer(img_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
        
        # YOLO Detection only
        results = yolo(frame, classes=0, conf=0.5)  # Only people, 50% confidence
        
        # Format results
        boxes = results[0].boxes.xyxy.tolist() if results[0].boxes else []
        
        return {
            "timestamp": data["timestamp"],
            "yolo_count": len(boxes),
            "boxes": boxes,
            "edge_data": {
                "count": data.get("count", 0),
                "device_id": data.get("device_id")
            }
        }
    
    except Exception as e:
        print(f"Processing error: {str(e)}")
        return None