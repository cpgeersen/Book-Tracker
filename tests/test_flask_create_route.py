from app import  create_app

def test_flask_route():
    app = create_app()
    client = app.test_client()
    response = client.get('/api/test')
    assert response.get_json() == {'status': 'ok'}
    assert response.status_code == 200
