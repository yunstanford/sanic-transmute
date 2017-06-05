from functools import wraps
from transmute_core.exceptions import APIException, NoSerializerFound
from transmute_core.function.signature import NoDefault
from transmute_core import ParamExtractor, NoArgument
from sanic.response import HTTPResponse
from sanic.exceptions import SanicException


DEFAULT_HTTP_CONTENT_TYPE = "application/octet-stream"


def create_handler(transmute_func, context):

    @wraps(transmute_func.raw_func)
    async def handler(request, *args, **kwargs):
        exc, result = None, None
        try:
            args, kwargs = await extract_params(request, context,
                                                transmute_func)
            result = await transmute_func.raw_func(*args, **kwargs)
        except SanicException as se:
            code = se.status_code or 400
            exc = APIException(message=str(se), code=code)
        except Exception as e:
            exc = e
        content_type = request.headers.get("Content-Type", DEFAULT_HTTP_CONTENT_TYPE)
        response = transmute_func.process_result(
            context, result, exc, content_type
        )
        return HTTPResponse(
            status=response["code"],
            content_type=response["content-type"],
            headers=response["headers"],
            body_bytes=response["body"],
        )
    handler.transmute_func = transmute_func
    return handler



async def extract_params(request, context, transmute_func):
    body = request.body
    content_type = request.headers.get("Content-Type", DEFAULT_HTTP_CONTENT_TYPE)
    extractor = ParamExtractorSanic(request, body)
    return extractor.extract_params(
        context, transmute_func, content_type
    )


class ParamExtractorSanic(ParamExtractor):

    def __init__(self, request, body):
        self._request = request
        self._body = body

    def _get_framework_args(self):
        return {"request": self._request}

    @property
    def body(self):
        return self._body

    def _query_argument(self, key, is_list):
        if key not in self._request.args:
            return NoArgument
        if is_list:
            return self._request.args.getlist(key)
        else:
            return self._request.args.get(key)

    def _header_argument(self, key):
        return self._request.headers.get(key, NoArgument)

    def _path_argument(self, key):
        kargs = self._request.app.router.get(self._request)[2]
        return kargs.get(key, NoArgument)
