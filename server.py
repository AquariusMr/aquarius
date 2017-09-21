from httptools import HttpParserError, HttpRequestParser
import asyncio

from request import Request


class HttpProtocol(asyncio.Protocol):

    def __init__(self):
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
        raise Exception("start_response not achieved")

    async def start_response(self, transport, request):
        raise Exception("start_response not achieved")
