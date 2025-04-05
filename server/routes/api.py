from flask import Blueprint, jsonify, request, current_app
from datetime import datetime
import zlib
import json


from advanced_analytics.processor import process_advanced_analytics
from .sse import broadcast_event

api_blueprint = Blueprint('api', __name__)
@api_blueprint.route('/receive_data', methods=['POST'])
def receive_data():
    """Unified endpoint for all edge device data"""
    try:
        # Decompress data
        compressed_data = request.data
        json_data = zlib.decompress(compressed_data).decode('utf-8')
        data = json.loads(json_data)

        # Common validation
        required_fields = ['count', 'timestamp']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Ensure timestamp is string
        if isinstance(data['timestamp'], str):
            try:
                dt = datetime.fromisoformat(data['timestamp'])
                data['timestamp'] = dt.isoformat()
            except ValueError:
                data['timestamp'] = datetime.utcnow().isoformat()
        else:
            data['timestamp'] = datetime.utcnow().isoformat()
        
        # Enhance data
        data.update({
            'device_id': request.headers.get('X-Device-ID', 'unknown'),
            'received_at': datetime.utcnow().isoformat(),
            'density': data.get('count', 0) / data.get('area', 10)
        })
        
        # SINGLE INSERT OPERATION
        db = current_app.db
        inserted = db.crowd_data.insert_one(data)
        data['_id'] = str(inserted.inserted_id)  # Add string ID to data
        
        # Broadcast to frontend
        broadcast_event('crowd_update', {
            'type': 'crowd_data',
            'data': data
        })
        
        return jsonify({'status': 'success'}), 200
    
    except Exception as e:
        current_app.logger.error(f"Receive error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_blueprint.route('/advanced_analysis', methods=['POST'])
def handle_advanced_analysis():
    """Dedicated endpoint for frame processing"""
    try:
        if not request.data:
            return jsonify({"error": "No data provided"}), 400
            
        data = json.loads(zlib.decompress(request.data))
        
        # Validate frame data
        if "full_frame" not in data:
            return jsonify({"error": "Missing frame data"}), 400

        # Process with YOLO
        result = process_advanced_analytics(data)
        if not result:
            return jsonify({"error": "Processing failed"}), 500

        # Store in MongoDB
        db = current_app.db
        result['processed_at'] = datetime.utcnow()
        db_result = db.analytics.insert_one(result)
        
        # Broadcast to frontend
        broadcast_event('analytics_update', {
            'type': 'advanced_analytics',
            'data': result,
            'inserted_id': str(db_result.inserted_id)
        })
        
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        current_app.logger.error(f"Advanced analysis error: {str(e)}")
        return jsonify({"error": str(e)}), 500