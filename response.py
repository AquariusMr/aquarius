"""
server
"""
import copy
import uuid

try:
    import ujson as json
except ImportError:
    import json


class BaseResponse(object):
    """Response"""

    __solts__ = ("_response", "format_kwargs", "_cookie")

    def __init__(self):
        self._cookie = []
        self._response = [
            b'HTTP/1.1 %(status)d \r\n',
            b'Content-Type: %(content_type)s; charset=utf-8\r\n',
            b'Server: aquarius\r\n',
            b'',
            b'Content-Length:%(length)d\r\n\r\n',
            b'%(body)s\r\n\r\n']

        self.format_kwargs = {b"status": 200, b"content_type": b"text/html"}

    @property
    def response(self):

        if self._cookie:
            self._response[3] = b"".join(self._cookie)
            self._cookie[:] = []

        return b"".join(self._response)

    def set_cookie(self, name, value, path="/"):
        """set_cookie"""
        cookie_parameter = {}
        cookie_parameter[b'key'] = self.to_bytes(name)
        cookie_parameter[b'value'] = self.to_bytes(value)
        cookie_parameter[b'path'] = self.to_bytes(path)
        cookie_bytes = b'Set-cookie: %(key)s=%(value)s; path=%(path)s\r\n'
        cookie = cookie_bytes % cookie_parameter
        self._cookie.append(cookie)

        return self

    def to_bytes(self, string):
        """str to bytes"""
        if isinstance(string, bytes):
            return string
        return bytes(string, encoding='utf-8')

    def __call__(self, content, request=None, token_name="aquariusid", **kwargs):
        """__call__(self, content, request=None, **kwargs)
        request must have then can set uuid cookie.
        """
        if request and not request.has_token:
            self.set_cookie(token_name, str(uuid.uuid1()))

        format_kwargs_init = copy.deepcopy(self.format_kwargs)

        if isinstance(content, dict):
            content = json.dumps(content)
            format_kwargs_init.update({b"content_type": b"application/json"})

        body = self.to_bytes(content)
        length = len(body)

        format_kwargs_init.update({b"body": body, b"length": length})

        if kwargs:

            header = {
                self.to_bytes(key):
                (value if isinstance(value, int) else self.to_bytes(value))
                for key, value in kwargs.items()
            }

            format_kwargs_init.update(header)

        response_bytes = self.response % format_kwargs_init

        return response_bytes


HttpResponse = BaseResponse()
