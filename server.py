import re

import asyncio
from httptools import HttpParserError, HttpRequestParser
from request import Request

class RouterError(Exception): pass

class HttpProtocol(asyncio.Protocol):

    __slots__ = ("_route", "_loop", "_transport", "_parser", "_request")

    def __init__(self, event_loop=None, route=None, re_route=None):
        self._route = route
        self._re_route = re_route
        self._loop = event_loop
        self._transport = None
        self._parser = HttpRequestParser(self)
        self._request = Request()

    def connection_made(self, transport):
        self._transport = transport

    def data_received(self, data):
        try:
            self._parser.feed_data(data)
        except HttpParserError:
            pass

    def connection_lost(self, exc):
        self._transport.close()

    def on_url(self, uri):
        self._request.uri = uri.decode()

    def on_header(self, name, value):
        self._request.headers[name] = value

    def on_headers_complete(self):

        self._request.version = self._parser.get_http_version()
        self._request.method = self._parser.get_method().decode()

    def on_body(self, body):
        self._request.body.append(body)

    def on_message_complete(self):
        if self._request.body:
            self._request.body = b"".join(self._request.body)

        self._loop.create_task(
            self.start_response(request=self._request, transport=self._transport)
        )

    async def start_response(self, transport, request):

        try:
            _view = self._route.get(request.url, self._re_route)

            if isinstance(_view, list):
                for _re_route_tuple in _view:

                    regex, nums, view = _re_route_tuple
                    _re_uri = re.match(regex, request.url)

                    if _re_uri:
                        args = [_re_uri.group(i+1) for i in range(nums)]
                        content = await view(request, *args)
                        break
                else:
                    print(request.url)
                    raise RouterError("404 %s" % request.url)
            else:
                content = await _view(request)

            transport.write(content)
        except RouterError:
            transport.write(b'HTTP/1.1 404 Not Found\r\nServer: aquarius\r\nContent-Length:9\r\n\r\nNot Found\r\n\r\n')
        except ValueError:
            transport.write(b'HTTP/1.1 404 Not Found\r\nServer: aquarius\r\nContent-Length:9\r\n\r\nNot Found\r\n\r\n')
        except AttributeError:
            transport.write(b'HTTP/1.1 404 Not Found\r\nServer: aquarius\r\nContent-Length:9\r\n\r\nNot Found\r\n\r\n')

        if request.version == "1.0":
            transport.close()


if __name__ == "__main__":
    import uvloop
    from functools import partial

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    HttpProtocol = partial(HttpProtocol, loop)
    server_coro = loop.create_server(HttpProtocol, "0.0.0.0", "8002")
    server = loop.run_until_complete(server_coro)
    loop.run_until_complete(server.wait_closed())
