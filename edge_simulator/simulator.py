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
        """Send data to server with compression"""
        data = self.generate_data()
        
        try:
            # Compress the data
            compressed = zlib.compress(json.dumps(data).encode())
            
            # Send to server
            response = requests.post(
                f"{self.server_url}/api/receive_data",
                data=compressed,
                headers={
                    "Content-Type": "application/json",
                    "Content-Encoding": "gzip",
                    "X-Device-ID": self.device_id
                },
                timeout=2
            )
            
            print(f"Data sent - Status: {response.status_code}, Count: {data['count']}")
            return response.status_code == 200
        
        except Exception as e:
            print(f"Failed to send data: {e}")
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