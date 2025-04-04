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
        """Generate simulated crowd data"""
        return {
            "device_id": self.device_id,
            "count": random.randint(0, 50),
            "location": random.choice(self.locations),
            "area": random.uniform(5, 20),  # Area in square meters
            "timestamp": datetime.now().isoformat()
        }
    
    def send_data(self):
        data = self.generate_data()
        try:
            # Ensure proper encoding
            json_data = json.dumps(data).encode('utf-8')
            compressed = zlib.compress(json_data)
            
            response = requests.post(
                f"{self.server_url}/api/advanced_analysis",
                data=compressed,
                headers={
                    "Content-Type": "application/json",
                    "Content-Encoding": "gzip",
                    "X-Device-ID": self.device_id,
                    "Connection": "keep-alive"  # Prevent resets
                },
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"Error {response.status_code}: {response.text}")
            return response.status_code == 200
            
        except requests.exceptions.ConnectionError as e:
            print(f"Connection failed: {str(e)}")
            time.sleep(5)  # Wait before retry
            return False
        
    def run(self, interval=5):
        """Run continuous simulation"""
        print(f"Starting edge device simulator (ID: {self.device_id})")
        while True:
            self.send_data()
            time.sleep(interval)

if __name__ == "__main__":
    simulator = EdgeDeviceSimulator("http://localhost:5000")
    simulator.run()