import time
import random
import zlib
import json
import requests
from datetime import datetime

class EdgeDeviceSimulator:
    def __init__(self, server_url):
        self.server_url = server_url
        self.locations = ["Main Entrance", "Food Court", "Exit Gate", "Parking Lot"]
        self.device_id = f"device_{random.randint(1000, 9999)}"
    
    def generate_data(self):
        """Generate simulated crowd data with JSON-serializable timestamp"""
        return {
            "device_id": self.device_id,
            "count": random.randint(0, 50),
            "location": random.choice(self.locations),
            "area": random.uniform(5, 20),
            "timestamp": datetime.now().isoformat()  # Convert to string
        }
    
    # Modify the send_data method to use /receive_data endpoint for basic data
    def send_data(self):
        data = self.generate_data()
        try:
            json_data = json.dumps(data).encode('utf-8')
            compressed = zlib.compress(json_data)
            
            # Use /receive_data for basic crowd data
            response = requests.post(
                f"{self.server_url}/api/receive_data",  # Changed endpoint
                data=compressed,
                headers={
                    "Content-Type": "application/json",
                    "Content-Encoding": "gzip",
                    "X-Device-ID": self.device_id
                },
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"Error {response.status_code}: {response.text}")
            return response.status_code == 200
            
        except Exception as e:  # Broadened exception handling
            print(f"Error: {str(e)}")
            time.sleep(5)
            return False
        
    # In simulator.py, add this method for testing advanced analytics
    def send_advanced_data(self):
        data = {
            "device_id": self.device_id,
            "count": random.randint(0, 50),
            "full_frame": "base64encodedframedata",  # Mock frame
            "timestamp": datetime.now().isoformat()
        }
        self._send_data(data, "/api/advanced_analysis")
        
    def run(self, interval=5):
        """Run continuous simulation"""
        print(f"Starting edge device simulator (ID: {self.device_id})")
        while True:
            self.send_data()
            time.sleep(interval)

if __name__ == "__main__":
    simulator = EdgeDeviceSimulator("http://localhost:5000")
    simulator.run()