from httptools import HttpParserError, HttpRequestParser
import asyncio
import uvloop

from request import Request


class HttpProtocol(asyncio.Protocol):
    __slost__ = ("_loop", "_transport",  "_parse", "_request")

    def __init__(self):
        self._loop = asyncio.get_event_loop()
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

    def run(self, **kwargs):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        try:
            self._loop.run_until_complete(self._loop.create_server(HttpProtocol, **kwargs))
            self._loop.run_forever()
        except KeyboardInterrupt:
            print("server is closing, byebye!")
            self._loop.stop()

    def on_message_complete(self):
        if self._request.body:
            self._request.body = b"".join(self._request.body)

        self._loop.create_task(
            self.start_response(request=self._request, transport=self._transport)
        )

    async def start_response(self, transport, request):
        print("start_response")
        try:
            view = self.Route_Config.get(request.url)(request)
            if not isinstance(view, bytes) or hasattr(view, "__await__"):
                view = await view

            transport.write(view)
        except TypeError:
            # print(request.url, "NOT FOUND VIEW")
            transport.write(b'HTTP/1.1 404 Not Found\r\nContent-Length:9\r\n\r\nNot Found\r\n\r\n')
        finally:
            if request.version == "1.0":
                transport.close()

    def route(self, path):

        def _inner(func):
            Route_Config.update({path: func})
        return _inner


if __name__ == '__main__':

    Route_Config = {}

    app = HttpProtocol()

    @app.route("/")
    async def test(request):
        return b'HTTP/1.1 404 Not Found\r\nContent-Length:9\r\n\r\nNot Found\r\n\r\n'

    app.run(port=8002, host="0.0.0.0")