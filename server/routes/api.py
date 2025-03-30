from flask import Blueprint, jsonify, request
from datetime import datetime
import zlib
import json
from .sse import add_event  # Import SSE helper

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/receive_data', methods=['POST'])
def receive_data():
    """Endpoint for edge devices to send compressed crowd data"""
    try:
        # Decompress the data (matches your edge device code)
        compressed_data = request.data
        json_data = zlib.decompress(compressed_data).decode('utf-8')
        data = json.loads(json_data)
        
        # Validate required fields
        if 'count' not in data or 'timestamp' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Add device info
        data['device_id'] = request.headers.get('X-Device-ID', 'unknown')
        
        # Calculate density if not provided
        if 'density' not in data:
            area = data.get('area', 10)  # default 10 sqm
            data['density'] = data['count'] / area
        
        # Here you would normally save to MongoDB
        # For this example, we'll just add to event store
        add_event({
            'type': 'crowd_data',
            'data': data
        })
        
        return jsonify({'status': 'success'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500