import cv2
import numpy as np

class HeatmapGenerator:
    def __init__(self, grid_size=(20, 20)):
        self.grid_size = grid_size
    
    def generate(self, frame, tracks):
        h, w = frame.shape[:2]
        grid = np.zeros(self.grid_size)
        
        for track in tracks:
            x1, y1, x2, y2 = track.to_ltrb()
            cx, cy = int((x1+x2)/2 * self.grid_size[0]/w), int((y1+y2)/2 * self.grid_size[1]/h)
            if 0 <= cx < self.grid_size[0] and 0 <= cy < self.grid_size[1]:
                grid[cy, cx] += 1
                
        return grid.tolist()