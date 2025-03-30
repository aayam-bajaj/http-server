from flask import Blueprint, request, jsonify
from app.models import CrowdData
from datetime import datetime
import zlib
import json

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/receive_data', methods=['POST'])
def receive_data():
    try:
        if 'Content-Encoding' in request.headers and request.headers['Content-Encoding'] == 'gzip':
            data = json.loads(zlib.decompress(request.data).decode('utf-8'))
        else:
            data = request.get_json()
        
        crowd = CrowdData(
            device_id=data.get('device', 'raspberry_pi'),
            people_count=data['count'],
            detections=data['detections'],
            is_anomaly=data['count'] > 10
        )
        crowd.save()
        
        return jsonify({'status': 'success'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_blueprint.route('/get_data', methods=['GET'])
def get_data():
    limit = int(request.args.get('limit', 100))
    data = CrowdData.objects.order_by('-timestamp').limit(limit)
    return jsonify([{
        'timestamp': item.timestamp.isoformat(),
        'count': item.people_count,
        'anomaly': item.is_anomaly,
        'detections': item.detections
    } for item in data])