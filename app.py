import asyncio
import uvloop
from server import HttpProtocol


class Aquarius(HttpProtocol):

    _loop = asyncio.get_event_loop()
    _route_config = {}

    def __init__(self, name=None):
        super(Aquarius, self).__init__()
        self.name = name

    def run(self, **kwargs):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        try:
            self._loop.run_until_complete(self._loop.create_server(Aquarius, **kwargs))
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
        try:
            view = self._route_config.get(request.url)(request)
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
            self._route_config.update({path: func})
        return _inner
