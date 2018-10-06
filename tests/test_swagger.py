import json


async def test_swagger_page(test_cli):
    response = await test_cli.get(
            '/api/v1/',
        )
    assert response.status == 200
    assert "text/html" == response.headers["Content-Type"]


async def test_swagger_json(test_cli):
    response =  await test_cli.get('/api/v1/swagger.json')
    assert 200 == response.status
    assert "application/json" == response.headers["Content-Type"]
    text = await response.text()
    assert json.loads(text)["paths"]["/multiply"]["get"]["responses"] == {
        "200": {
            "schema": {"type": "integer"},
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
