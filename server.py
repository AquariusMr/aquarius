import re
import time

from httptools import HttpParserError, HttpRequestParser
import asyncio

from request import Request


class HttpProtocol(asyncio.Protocol):

    __slots__ = ("_route", "_loop", "_transport", "_parser", "_request", "_response")

    def __init__(self, loop=None, route=None, Response=None):
        self._route = route
        self._loop = loop
        self._transport = None
        self._parser = HttpRequestParser(self)
        self._request = Request()
        self._response = Response

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
            _route = self._route.get(request.url, self._route["__re__"])

            if isinstance(_route, list):
                for route in _route:
                    rec, groups, func = route
                    re_res = re.match(rec, request.url)
                    if re_res:
                        args = []

                        for i in range(groups):
                            args.append(re_res.group(i+1))

                        content = await func(request, *args)

                        break
                else:
                    raise Exception("404 %s" % request.url)
            else:
                content = await _route(request)

            transport.write(self._response(content))
        except Exception as e:
            print(e, time.ctime(), transport.get_extra_info("socket"))
            transport.write(b'HTTP/1.1 404 Not Found\r\nServer: aquarius\r\nContent-Length:9\r\n\r\nNot Found\r\n\r\n')
        if request.version == "1.0":
            transport.close()


if __name__ == "__main__":
    import uvloop
    from functools import partial

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    HttpProtocol = partial(HttpProtocol, loop)
    print(HttpProtocol)
    server_coro = loop.create_server(HttpProtocol, "0.0.0.0", "8002")
    server = loop.run_until_complete(server_coro)
    loop.run_until_complete(server.wait_closed())





