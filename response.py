try:
    import ujson as json
except ImportError:
    import json


__all__ = ["ResponseBase"]


RESPONSE_HERD = (
    "HTTP/1.1 {status}\r\n"
    "Content-Type: {content_type}; charset=utf-8\r\n"
    "Server: {server}\r\n"
    "{cookie}"
    "Content-Length:{length}\r\n\r\n"
)


class ResponseBase:

    def __init__(self, status_code: int=200, body: str=None, body_type=None):

        self.status_code = status_code
        self.body = body
        self.body_type = body_type

        self._cookie = []

    def bytes_response(self):
        body = bytes(self.body, encoding='utf-8')
        nums_body = len(body)

        set_hd = RESPONSE_HERD.format(
            status=self.status_code,
            content_type=self.body_type,
            server="aquarius",
            cookie=self.__cookie_set(),
            length=nums_body
        )
        return bytes(set_hd, encoding='utf-8') + body + b'\r\n\r\n'

    def set_cookie(self, key, value, path="/"):
        cookie = 'Set-cookie: %(key)s=%(value)s; path=%(path)s\r\n' % {"key": key, "value": value, "path": path}
        self._cookie.append(cookie)
        return self

    def __cookie_set(self): return "".join(self._cookie)

    def __repr__(self): return "<%s : %s>" % (self.__class__.__name__, str(self.status_code))

    def __str__(self): return self.bytes_response().decode('utf-8')


class HTTPResponse(ResponseBase):
    def __call__(self, content):
        self.body = content

        if isinstance(content, (dict, list, tuple)):
            self.body = json.dumps(content)
            self.body_type = 'application/json'

        elif isinstance(content, str):
            self.body = content
            self.body_type = 'text/html'

        return self.bytes_response()
