import sys
import re
import uuid
import asyncio
import uvloop
from functools import partial

from server import HttpProtocol
from request import Request
from response import HttpResponse


class Aquarius:

    def __init__(self, name=None, protocol=HttpProtocol, token=True):
        self._name = name
        self._protocol = protocol
        self._route_config = {}
        self._re_route_config = []
        self._loop = None

        self._token = True

    def run(self, host="0.0.0.0", port=8002, **kwargs):

        HttpProtocol = self._protocol

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

        loop = asyncio.get_event_loop()
        self._loop = loop

        HttpProtocol = partial(HttpProtocol, loop, self._route_config, self._re_route_config,
                                self.to_response, self._token)
        for _route_set in self._route_config.items():
            print(_route_set)
        for _route_set_re in self._re_route_config:
            print(_route_set_re)

        server_coro = loop.create_server(HttpProtocol, host=host, port=port, **kwargs)
        server = loop.run_until_complete(server_coro)
        try:
            loop.run_until_complete(server.wait_closed())
        except KeyboardInterrupt:
            print("\r\nserver is closing")
        finally:
            loop.close()

    def route(self, path):
        groups = path.count("(")
        regex = re.compile("^" + path+ "$")

        def _inner(func):

            if func.__name__.lower() != func.__name__:
                func_obj = func()
                if groups == 0:
                    self._route_config.update({path: func_obj})
                if groups > 0:
                    self._re_route_config.append((regex, groups, func_obj))

            else:
                if groups == 0:
                    self._route_config.update({path: func})
                if groups > 0:
                    self._re_route_config.append((regex, groups, func))

        return _inner

    def to_response(self, content):

        if isinstance(content, str):
            return HttpResponse(content)

        return content

    def to_template(self, content):
        pass

    def exec_task(self, coro):
        """add a HTTPRequest task"""
        return self._loop.create_task(coro)

    async def sleep(self, time, callback = None, *args, **kwargs):
        """a coro func that exec later time"""

        await asyncio.sleep(time)

        if callback:
            return callback(*args, **kwargs)

    def awaiting(self, time):
        """let func became a coro await time"""

        def _init_set_wraper(func):

            async def _async_wrapper(*args, **kwargs):

                await asyncio.sleep(time)
                return func(*args, **kwargs)

            return _async_wrapper

        return _init_set_wraper

    class View:

        def __repr__(self):
            return self.__class__.__name__

        async def __call__(self, request, *args, **kwargs):
            self.request = request
            if request.method == "GET":
                res = self.get(*args, **kwargs)

                if isinstance(res, bytes):
                    return res
                else:
                    return await res

            elif request.method == "POST":
                res = await self.post(*args, **kwargs)

                if isinstance(res, bytes):
                    return res
                else:
                    return await res
            else:
                res = ""
                return res

        def get(self, *args, **kwargs):
            return HttpResponse("GET")

        def post(self, *args, **kwargs):
            return HttpResponse("POST")


if __name__ == '__main__':

    from already_sql import *
    from response import HttpResponse
    from fetch import HTTPRequest


    app = Aquarius(__name__)

    @app.route("/")
    async def index(request):
        return HttpResponse({"errcode": 0, "errmsg": "aquarius"}, request=request)

    @app.route("/view(\d)")
    class Auther(app.View):

        async def get(self, idt):
            return HttpResponse("view hello")


    @app.route("/view(\d)(\d)")
    class AutherView(app.View):

        def get(self, idt, pk):
            return HttpResponse("view hello2")

    app.run()
