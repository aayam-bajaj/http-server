from flask import Blueprint, render_template

views_blueprint = Blueprint('views', __name__)

@views_blueprint.route('/')
def dashboard():
    """Render the main dashboard"""
    return render_template('index.html')

@views_blueprint.route('/map')
def map_view():
    """Render the map view"""
    return render_template('map.html')