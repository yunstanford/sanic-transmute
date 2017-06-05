import json


def test_route_content_type_in_response(app):
    request, response = app.test_client.get(
            '/api/v1/user/yun',
        )
    assert response.status == 200
    assert response.headers["Content-Type"] == "application/json"


def test_route_headers(app):
    request, response = app.test_client.get(
            '/api/v1/headers/',
        )
    assert response.status == 200
    assert response.headers["location"] == "foooo"


def test_route_multiply(app):
    request, response = app.test_client.get(
            '/multiply?left=3&&right=4',
        )
    assert response.status == 200
    res = response.text
    assert json.loads(res) == 12


def test_route_multiply_bad_int(app):
    request, response = app.test_client.get(
            '/multiply?left=hello&&right=False',
        )
    assert response.status == 400


def test_route_raise_error(app):
    request, response = app.test_client.get(
            '/killme',
        )
    assert response.status == 500
    error_msg = response.text
    assert 'Something bad happened' in error_msg


def test_route_api_exception(app):
    request, response = app.test_client.get(
            '/api/v1/user/missing',
        )
    assert response.status == 404
    error_msg = response.text
    assert 'Something bad happened' in error_msg


def test_route_body_and_header_params(app):
    request, response = app.test_client.post('/body_and_header',
                          data=json.dumps({"body": "body"}),
                          headers={
                              "content-type": "application/json",
                              "header": "header"
                          })
    assert 200 == response.status
    return_value = response.text
    assert json.loads(return_value) == False


def test_route_blueprint_multiply(app):
    request, response = app.test_client.get(
            '/blueprint/multiply?left=3&&right=4',
        )
    assert response.status == 200
    res = response.text
    assert json.loads(res)== "3*4=12"
