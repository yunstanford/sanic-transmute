import json


def test_parsing_path_parameters(app):
    request, response = app.test_client.get(
            '/api/v1/user/yun',
        )
    assert response.status == 200
    user = response.text
    assert json.loads(user) == "yun"


def test_parsing_path_parameters_list(app):
    request, response = app.test_client.get(
            '/api/v1/group/?group=velocity&group=mondev',
        )
    assert response.status == 200
    user = response.text
    assert json.loads(user) == "mondev,velocity"


def test_parsing_parameters_optional(app):
    request, response = app.test_client.get(
            '/api/v1/env/',
        )
    assert response.status == 200
    exist = response.text
    assert json.loads(exist) == False


def test_parsing_parameters_optional_with_value(app):
    request, response = app.test_client.get(
            '/api/v1/env/?exist=True',
        )
    assert response.status == 200
    exist = response.text
    assert json.loads(exist) == True


def test_parsing_query_parameters(app):
    request, response = app.test_client.get(
            '/multiply?left=3&right=4',
        )
    assert response.status == 200
    result = response.text
    assert json.loads(result) == 12
