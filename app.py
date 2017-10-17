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
        return self._loop.create_task(coro)


if __name__ == '__main__':

    from already_sql import *
    from fetch import HTTPRequest


    app_sql = MysqlAlready("127.0.0.1", "root", "mysql", "test")

    app = Aquarius(__name__)

    @app.route("/")
    async def test(request):
        result = await app.exec_task(HTTPRequest("www.baidu.com")("GET"))
        return HttpResponse.set_cookie("name", "shihongguang")(result)

    app.run()
