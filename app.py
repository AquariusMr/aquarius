import sys
import asyncio
import uvloop
from functools import partial

from server import HttpProtocol
from request import Request
from response import HttpResponse


class Aquarius:

    def __init__(self, name=None, protocol=HttpProtocol):
        self._name = name
        self._protocol = protocol
        self._route_config = {}
        self._loop = None

    def run(self, host="0.0.0.0", port=8002, **kwargs):

        HttpProtocol = self._protocol

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

        loop = asyncio.get_event_loop()
        self._loop = loop

        HttpProtocol = partial(HttpProtocol, loop, self._route_config, 
            self.to_response)
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
            self._route_config.update({path: func})
        return _inner

    def to_response(self, content):

        if isinstance(content, (str, dict)):
            return HttpResponse(content)
        elif isinstance(content, (tuple, list)):
            try:
                return HttpResponse(content[0], **content[1])
            except Exception as e:
                return HttpResponse("Bad Server", status=500)
        else:
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


if __name__ == '__main__':

    from already_sql import *
    from response import HttpResponse
    from fetch import HTTPRequest


    app_sql = MysqlAlready("127.0.0.1", "root", "mysql", "test")

    app = Aquarius(__name__)

    @app.route("/")
    async def index(request):
        result = await app.exec_task(HTTPRequest("www.baidu.com")("GET"))

        @app.awaiting(3)
        def printf(name):
            print(name)

        await printf("shihongguang")

        return HttpResponse.set_cookie("name", "shihongguang")(result)

    app.run()
