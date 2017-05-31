from sanic import Sanic
from sanic.response import json

app = Sanic()

@app.route("/<path_param>/")
async def test(request, path_param):
    return json(
    	{
    		"path_params": request.app.router.get(request)[2],
    		"header_params": request.headers,
    		"query_params": request.args,
    		"body": request.body,
    	}
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
