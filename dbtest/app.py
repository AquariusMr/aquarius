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

    def run(self, host="0.0.0.0", port=8002, orm=None, **kwargs):

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

    def orm_setting(self):

        if self._name:
            __file__ = os.path.dirname(os.path.dirname(os.path.abspath(self._name)))
            sys.path.append(__file__)

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "db.settings")
        import django
        django.setup()


if __name__ == '__main__':

    from response import json_response as response

    app = Aquarius(__name__)
    app.orm_setting()

    from auther.models import Auther

    @app.route("/")
    async def test(request):
        # print(request.url)
        # auther_obj = Auther()
        # auther_obj.save()
        Auther.objects.all()
        return response({"name": "shihongguang", "age": 25 , "gender": 0, "language": "python"})

    app.run()

