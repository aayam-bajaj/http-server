# from flask import Flask
# from flask_cors import CORS
# from pymongo import MongoClient
# from routes.api import api_blueprint
# from routes.sse import sse_blueprint
# from routes.views import views_blueprint
# import os

# app = Flask(__name__)
# CORS(app)

# # MongoDB Configuration
# mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
# client = MongoClient(mongo_uri)
# app.db = client['crowd_monitoring']

# # Register Blueprints
# app.register_blueprint(api_blueprint, url_prefix='/api')
# app.register_blueprint(sse_blueprint, url_prefix='/sse')
# app.register_blueprint(views_blueprint)

# @app.route('/health')
# def health_check():
#     return {'status': 'healthy'}

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from routes.api import api_blueprint
from routes.sse import sse_blueprint
from routes.views import views_blueprint
import os

app = Flask(__name__)
CORS(app)

# MongoDB Configuration
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(mongo_uri)
app.db = client['crowd_monitoring']
app.sse=sse_blueprint

# In app.py, after MongoDB initialization
try:
    # Verify MongoDB connection
    app.db.command('ping')
    print("✅ MongoDB connection successful")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    # Handle connection error appropriately

# Register Blueprints
app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(sse_blueprint, url_prefix='/sse')
app.register_blueprint(views_blueprint)

@app.route('/health')
def health_check():
    return {'status': 'healthy'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True,use_reloader=False)