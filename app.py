import os
import sys
import asyncio
import uvloop
from functools import partial

from server import HttpProtocol
from request import Request


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
        try:
            loop.run_until_complete(server.wait_closed())
        except KeyboardInterrupt:
            print("\r\nserver is closing")
        finally:
            loop.close()

    def route(self, path):

        def _inner(func):
            if not self.is_coroutine(func):
                func = asyncio.coroutine(func)
            self._route_config.update({path: func})
        return _inner

    @staticmethod
    def is_coroutine(func):
        try:
            coro_or_func = func(Request)
            result = hasattr(coro_or_func, "__await__")
            if result:
                coro_or_func.close()
        finally:
            return result


if __name__ == '__main__':

    from response import json_response as response
    from celery_test import sendmail as send

    app = Aquarius(__name__)

    @app.route("/")
    async def test(request):
        task = send.delay(1234)
        return response({"key": task.id })

    app.run()
