import asyncio


class HTTPRequest(object):

    def __new__(cls, *args, **kwargs):

        if not hasattr(cls, "_instance"):
            cls._instance = super(HTTPRequest, cls).__new__(cls)

        return cls._instance

    def __init__(self, uri=None, method=None):
        self._request_header = ('%(method)s /%(uri)s HTTP/1.0\r\nHost: %(host)s\r\n\r\n')
        self._request_body = '%(body)s\r\n'

        self._uri = uri
        self._method = method

    def __call__(self, method=None, uri=None):
        if uri:
            self._uri = uri

        if method is None:
            pass
        elif method is "GET":
            return self.get(url)

        return self

    async def fetch(self, uri, port=80, method='GET'):

        host = uri.split("?", 1)[0]

        response_header = {}
        response_body = b''

        connect = asyncio.open_connection(uri, port)

        reader, writer = await connect

        request_string = self._request_header % {'method': 'GET', 'uri': uri , 'host': host}

        writer.write(request_string.encode('utf-8'))

        await writer.drain()

        response_line = await reader.readline()

        first_header = response_line.rstrip()
        response_header[b'first_line'] = first_header

        protocol, status = first_header.split(b' ', 1)
        response_header[b'protocol'] = protocol
        response_header[b'status'] = status

        while True:
            response_line = await reader.readline()

            if response_line == b'\r\n':
                break

            key , value= response_line.rstrip().split(b':', 1)
            response_header[key] = value.strip()

        while True:
            response_line = await reader.readline()

            if response_line == b'\r\n' or response_line == b'':
                break

            response_body = response_body + response_line.rstrip()

        writer.close()

        return {'header': response_header, 'body': response_body}

    async def get(self, uri=None, port=80):
        if uri is None:
            uri = self._uri if self._uri else "0.0.0.0"
        response = await self.fetch(uri, port=port)
        return response['body']

    async def post(self, uri, port=80, method='POST'):
        pass



if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    tasks = [HTTPRequest().get('0.0.0.0', 8000)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()