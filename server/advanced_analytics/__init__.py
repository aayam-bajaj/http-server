# import os
# from ultralytics import YOLO
# from deep_sort_realtime.deepsort_tracker import DeepSort
# from .heatmap import HeatmapGenerator
# from .anomaly import AnomalyDetector

# # Initialize models on import
# MODEL_DIR = os.path.join(os.path.dirname(__file__), "../../models")
# yolo = YOLO(os.path.join(MODEL_DIR, "yolov8n.pt"))
# # deepsort = DeepSort(
# #     model_path=os.path.join(MODEL_DIR, "deepsort_mars.pb"),
# #     max_age=30
# # )
# heatmap = HeatmapGenerator()
# anomaly = AnomalyDetector()

# In server/advanced_analytics/__init__.py
from ultralytics import YOLO
import os

# Initialize only YOLO
yolo = YOLO(os.path.join(os.path.dirname(__file__), "../../models/yolov8n.pt"))