from flask import Flask, jsonify
from mongoengine import connect
from config import Config
from routes.api import api_blueprint




app = Flask(__name__)
app.config.from_object(Config)
connect(host=app.config['MONGO_URI'])
app.register_blueprint(api_blueprint)

from mongoengine import OperationError, NotUniqueError

@app.errorhandler(OperationError)
def handle_mongo_error(e):
    return jsonify({'error': 'Database operation failed', 'details': str(e)}), 500

@app.errorhandler(NotUniqueError)
def handle_duplicate_error(e):
    return jsonify({'error': 'Duplicate data detected'}), 400

@app.route('/')
def dashboard():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)