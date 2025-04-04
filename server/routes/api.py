from flask import Blueprint, jsonify, request,current_app
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
    
from advanced_analytics.processor import process_advanced_analytics

# In routes/api.py - Fix the advanced_analysis endpoint
@api_blueprint.route('/advanced_analysis', methods=['POST'])
def handle_advanced_analysis():
    try:
        db=current_app.db
        db=current_app.sse
        # Add proper error handling for malformed data
        if not request.data:
            return jsonify({"error": "No data provided"}), 400
            
        data = json.loads(zlib.decompress(request.data))
        
        # Required field validation
        if "full_frame" not in data:
            return jsonify({"error": "Missing frame data"}), 400

        result = process_advanced_analytics(data)
        if not result:
            return jsonify({"error": "Processing failed"}), 500

        # Insert to MongoDB
        db.analytics.insert_one(result)
        
        # Broadcast via SSE
        sse.publish({
            "type": "crowd_update",
            "data": result
        }, type='crowd_data')
        
        return jsonify({"status": "success"}), 200
        
    except zlib.error:
        return jsonify({"error": "Invalid compressed data"}), 400
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500