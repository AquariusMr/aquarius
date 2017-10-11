try:
    import ujson as json
except ImportError:
    import json


class BaseResponse:

    __solts__ = ("_cookie", "_response", "format_kwargs")

    def __init__(self):
        self._cookie = []

        self._response = [
            b'HTTP/1.1 %(status)d OK\r\n',
            b'Content-Type: %(content_type)s; charset=utf-8\r\n',
            b'Server: aquarius\r\n',
            b'Content-Length:%(length)d\r\n\r\n',
            b'%(body)s\r\n\r\n']

        self.format_kwargs = {b"status": 200, b"content_type": b"text/html"}

    @property
    def response(self):
        if self._cookie:
            pass
        return b"".join(self._response)

    def set_cookie(self, name, value):
        pass

    def to_bytes(self, string):
        return bytes(string, encoding='utf-8')

    def __call__(self, content, **kwargs):

        if not isinstance(content, str):
            content = json.dumps(content)
            self.format_kwargs.update({b"content_type": b"application/json"})

        body = self.to_bytes(content)
        length = len(body)

        self.format_kwargs.update({b"body": body, b"length": length})

        if kwargs:

            header = {
                self.to_bytes(key): 
                (value if isinstance(value, int) else self.to_bytes(value)) 
                for key, value in kwargs.items()
            }

            self.format_kwargs.update(header)

        return self.response % self.format_kwargs


HttpResponse = BaseResponse()