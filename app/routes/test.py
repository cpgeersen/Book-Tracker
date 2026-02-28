from flask import Blueprint, jsonify

test_bp = Blueprint('test', __name__,  url_prefix='/api')

@test_bp.route('test')
def test_route_check():
    return jsonify({"status": "ok"}), 200