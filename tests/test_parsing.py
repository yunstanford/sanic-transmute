import pytest


@pytest.mark.asyncio
async def test_parsing_path_parameters(app):
    request, response = app.test_client.get(
            '/api/v1/user/yun',
        )
    assert response.status == 200
    user = await response.json()
    assert user == "yun"


@pytest.mark.asyncio
async def test_parsing_parameters_optional(app):
    request, response = app.test_client.get(
            '/api/v1/env/',
        )
    assert response.status == 200
    user = await response.json()
    assert user == False


@pytest.mark.asyncio
async def test_parsing_parameters_optional_with_value(app):
    request, response = app.test_client.get(
            '/api/v1/env/?exist=True',
        )
    assert response.status == 200
    user = await response.json()
    assert user == True


@pytest.mark.asyncio
async def test_parsing_query_parameters(app):
    request, response = app.test_client.get(
            '/multiply?left=3&right=4',
        )
    assert response.status == 200
    result = await response.json()
    assert result == 12
