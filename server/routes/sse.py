import queue
from flask import Blueprint, Response
import json
from datetime import datetime
from threading import Lock
import time

sse_blueprint = Blueprint('sse', __name__)

class MessageAnnouncer:
    def __init__(self):
        self.listeners = []
        self.lock = Lock()
    
    def listen(self):
        with self.lock:
            self.listeners.append(queue.Queue(maxsize=5))
            return self.listeners[-1]
    
    def announce(self, msg):
        with self.lock:
            for i in reversed(range(len(self.listeners))):
                try:
                    self.listeners[i].put_nowait(msg)
                except queue.Full:
                    del self.listeners[i]

announcer = MessageAnnouncer()

def format_sse(data: dict) -> str:
    """Ensure all datetime objects are converted"""
    def json_serializer(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
    
    return f"data: {json.dumps(data, default=json_serializer)}\n\n"

@sse_blueprint.route('/stream')
def stream():
    def event_stream():
        q = announcer.listen()
        while True:
            msg = q.get()
            yield msg
    
    return Response(event_stream(), mimetype='text/event-stream')

def broadcast_event(event_type, data):
    """Helper to broadcast events to all SSE clients"""
    msg = format_sse(data=json.dumps(data), event=event_type)
    announcer.announce(msg)