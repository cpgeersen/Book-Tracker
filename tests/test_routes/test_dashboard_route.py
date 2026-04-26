def test_analytics(client):
    response = client.get('/dashboard')
    assert response.status_code == 200