import re
import asyncio
import uvloop
from functools import partial

from server import HttpProtocol


class Aquarius:

    def __init__(self, name=None, protocol=HttpProtocol):
        self._name = name
        self._protocol = protocol
        self._route_config = {}
        self._re_route_config = []
        self._loop = None

    def run(self, host="0.0.0.0", port=8002):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        loop = asyncio.get_event_loop()

        self._loop = loop
        _protocol = partial(self._protocol, loop, self._route_config, self._re_route_config)

        server_coro = loop.create_server(_protocol, host=host, port=port)
        server = loop.run_until_complete(server_coro)
        try:
            loop.run_until_complete(server.wait_closed())
        except KeyboardInterrupt:
            print("\r\nserver is closing")
        finally:
            loop.close()

    def route(self, path):

        nums = path.count("(")
        compile_string = re.compile("^" + path + "$")

        def _inner(func):

            if nums == 0:
                self._route_config.update({path: func})
            else:
                self._re_route_config.append((compile_string, nums, func))

        return _inner

    def exec_task(self, coro):
        return self._loop.create_task(coro)

    @staticmethod
    async def sleep(time, callback=None, *args, **kwargs):

        await asyncio.sleep(time)

        if callback:
            return callback(*args, **kwargs)

    @staticmethod
    def awaiting(time):

        def _init_set_wrapper(func):

            async def _async_wrapper(*args, **kwargs):

                await asyncio.sleep(time)
                return func(*args, **kwargs)

            return _async_wrapper

        return _init_set_wrapper
