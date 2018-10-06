import json


async def test_parsing_path_parameters(test_cli):
    response = await test_cli.get(
            '/api/v1/user/yun',
        )
    assert response.status == 200
    user = await response.text()
    assert json.loads(user) == "yun"


async def test_parsing_path_parameters_list(test_cli):
    response = await test_cli.get(
            '/api/v1/group/?group=velocity&group=mondev',
        )
    assert response.status == 200
    user = await response.text()
    assert json.loads(user) == "mondev,velocity"


async def test_parsing_parameters_optional(test_cli):
    response = await test_cli.get(
            '/api/v1/env/',
        )
    assert response.status == 200
    exist = await response.text()
    assert json.loads(exist) == False


async def test_parsing_parameters_optional_with_value(test_cli):
    response = await test_cli.get(
            '/api/v1/env/?exist=True',
        )
    assert response.status == 200
    exist = await response.text()
    assert json.loads(exist) == True


async def test_parsing_query_parameters(test_cli):
    response = await test_cli.get(
            '/multiply?left=3&right=4',
        )
    assert response.status == 200
    result = await response.text()
    assert json.loads(result) == 12
