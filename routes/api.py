from flask import Blueprint, request, jsonify
from models import CrowdData
from datetime import datetime
import zlib
import json

api = Blueprint('api', __name__)

@api.route('/receive_data', methods=['POST'])
def receive_data():
    # Handle compressed data from edge device
    if 'Content-Encoding' in request.headers and request.headers['Content-Encoding'] == 'gzip':
        data = json.loads(zlib.decompress(request.data).decode('utf-8'))
    else:
        data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data received'}), 400

    # Save to MongoDB
    crowd = CrowdData(
        device_id=data.get('device', 'raspberry_pi'),
        people_count=data['count'],
        detections=data['detections'],
        is_anomaly=data['count'] > 10  # Your anomaly threshold
    )
    crowd.save()

    return jsonify({'status': 'success', 'saved_id': str(crowd.id)})

@api.route('/get_data', methods=['GET'])
def get_data():
    limit = int(request.args.get('limit', 100))
    data = CrowdData.objects.order_by('-timestamp').limit(limit)
    return jsonify([{
        'timestamp': item.timestamp.isoformat(),
        'count': item.people_count,
        'anomaly': item.is_anomaly,
        'detections': item.detections
    } for item in data])

@api.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'alive'})