try:
    import ujson as json
except ImportError:
    import json


class BaseResponse:

    __solts__ = ("_cookie", "BaseReponse__response")

    def __init__(self):
        self._cookie = []

        self.__response = [
            b'HTTP/1.1 %(status)d OK\r\n',
            b'Content-Type: %(content_type)s; charset=utf-8\r\n',
            b'Server: aquarius\r\n',
            b'Content-Length:%(length)d\r\n\r\n',
            b'%(body)s\r\n\r\n']

    @property
    def response(self):
        if self._cookie:
            pass
        return b"".join(self.__response)

    def set_cookie(self, name, value):
        pass

    def __call__(self, content, **kwargs):

        format_kwargs = {b"status": 200}


        if not isinstance(content, str):
            content = json.dumps(content)
            format_kwargs.update({b"content_type": b"application/json"})

        body = bytes(content, encoding='utf-8')
        length = len(body)

        format_kwargs.update({b"body":body, b"length": length})

        if kwargs:
            format_kwargs.update(kwargs)

        return self.response % format_kwargs


HttpResponse = BaseResponse()