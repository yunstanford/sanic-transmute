import json


async def test_route_content_type_in_response(test_cli):
    response = await test_cli.get(
            '/api/v1/user/yun',
        )
    assert response.status == 200
    assert response.headers["Content-Type"] == "application/json"


async def test_route_headers(test_cli):
    response = await test_cli.get(
            '/api/v1/headers/',
        )
    assert response.status == 200
    assert response.headers["location"] == "foooo"


async def test_route_multiply(test_cli):
    response = await test_cli.get(
            '/multiply?left=3&&right=4',
        )
    assert response.status == 200
    res = await response.text()
    assert json.loads(res) == 12


async def test_route_multiply_bad_int(test_cli):
    response = await test_cli.get(
            '/multiply?left=hello&&right=False',
        )
    assert response.status == 400


async def test_route_raise_error(test_cli):
    response = await test_cli.get(
            '/killme',
        )
    assert response.status == 500
    error_msg = await response.text()
    assert 'Something bad happened' in error_msg


async def test_route_api_exception(test_cli):
    response = await test_cli.get(
            '/api/v1/user/missing',
        )
    assert response.status == 404
    error_msg = await response.text()
    assert 'Something bad happened' in error_msg


async def test_route_body_and_header_params(test_cli):
    response = await test_cli.post('/body_and_header',
                          data=json.dumps({"body": "body"}),
                          headers={
                              "content-type": "application/json",
                              "header": "header"
                          })
    assert 200 == response.status
    return_value = await response.text()
    assert json.loads(return_value) == False


async def test_route_blueprint_multiply(test_cli):
    response = await test_cli.get(
            '/blueprint/multiply?left=3&&right=4',
        )
    assert response.status == 200
    res = await response.text()
    assert json.loads(res)== "3*4=12"
