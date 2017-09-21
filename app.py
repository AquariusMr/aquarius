import asyncio
import uvloop
from functools import partial

from server import HttpProtocol
from request import Request
from response import json_response


class Aquarius:

    def __init__(self, name=None, protocol=HttpProtocol):
        self._name = name
        self._protocol = protocol
        self._route_config = {}

    def run(self, host="0.0.0.0", port=8002, **kwargs):

        HttpProtocol = self._protocol

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        loop = asyncio.get_event_loop()

        HttpProtocol = partial(HttpProtocol, loop, self._route_config)
        print(HttpProtocol)

        server_coro = loop.create_server(HttpProtocol, host=host, port=port, **kwargs)
        server = loop.run_until_complete(server_coro)
        loop.run_until_complete(server.wait_closed())


    def route(self, path):

        def _inner(func):
            if not self.is_coroutine_func(func):
                func = asyncio.coroutine(func)
            self._route_config.update({path: func})
        return _inner

    @staticmethod
    def is_coroutine_func(func):
        return hasattr(func(Request()), "__await__")

if __name__ == '__main__':
    app = Aquarius(__name__)

    @app.route("/")
    def test(request):
        # print(request.url)
        return json_response({"name": "shihongguang"})

    app.run()
