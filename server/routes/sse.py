from flask import Blueprint, Response, jsonify
import json
import time
from datetime import datetime

sse_blueprint = Blueprint('sse', __name__)

# Simple in-memory event store (replace with Redis in production)
event_store = []

def event_stream():
    """Generator function for SSE"""
    last_id = 0
    while True:
        # Check for new events
        new_events = [e for e in event_store if e['id'] > last_id]
        for event in new_events:
            last_id = event['id']
            yield f"data: {json.dumps(event['data'])}\n\n"
        time.sleep(1)

@sse_blueprint.route('/stream')
def stream():
    """SSE endpoint for dashboard"""
    return Response(
        event_stream(),
        mimetype="text/event-stream",
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
    )

def add_event(data):
    """Add new event to the store"""
    event_store.append({
        'id': len(event_store) + 1,
        'data': data,
        'timestamp': datetime.now().isoformat()
    })