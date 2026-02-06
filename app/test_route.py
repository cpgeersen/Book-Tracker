from flask import jsonify

def create_flask_route(app):
    # Creates a basic test route that returns JSON with
    # a status of ok and 200
    @app.route('/test_route')
    def test_route():
        return jsonify(status='ok'), 200