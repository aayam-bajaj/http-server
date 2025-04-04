from . import yolo, deepsort

def process_frame(frame):
    if yolo is None:
        raise ValueError("Models not initialized")
    
    # YOLO detection
    results = yolo(frame, classes=0, conf=0.5)  # People only
    detections = [
        ([x1, y1, x2-x1, y2-y1], float(conf), 'person')
        for r in results
        for x1, y1, x2, y2, conf in [r.boxes.xyxy[0].tolist() + [r.boxes.conf[0].item()]]]
    
    # DeepSort tracking
    tracks = deepsort.update_tracks(detections, frame=frame)
    
    return tracks