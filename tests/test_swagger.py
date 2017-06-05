import json


def test_swagger_page(app):
    request, response = app.test_client.get(
            '/api/v1/',
        )
    assert response.status == 200
    assert "text/html" == response.headers["Content-Type"]


def test_swagger_json(app):
    request, response =  app.test_client.get('/api/v1/swagger.json')
    assert 200 == response.status
    assert "application/json" == response.headers["Content-Type"]
    text = response.text
    assert json.loads(text)["paths"]["/multiply"]["get"]["responses"] == {
        "200": {
            "schema": {"type": "number"},
            "description": "success"
        },
        "400": {
            "schema": {
                "title": "FailureObject",
                "type": "object",
                "required": ["success", "result"],
                "properties": {
                    "result": {"type": "string"},
                    "success": {"type": "boolean"}
                }
            },
            "description": "invalid input received"}
    }
