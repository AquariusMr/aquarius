import asyncio


class HTTPRequest(object):

    def __new__(cls, *args, **kwargs):

        if not hasattr(cls, "_instance"):
            cls._instance = super(HTTPRequest, cls).__new__(cls)

        return cls._instance

    def __init__(self, uri=None):
        self._request_header = ('%(method)s /%(path)s HTTP/1.0\r\n' 
                                'Host: %(host)s\r\n\r\n')
        self._request_body = '%(body)s\r\n'

        self._uri = uri

    @staticmethod
    def uri_parse(uri):
        uris = uri.rsplit('/', 1)

        if len(uris) > 1:
            path = uris[1]
        else:
            path = ''

        return {'host': uris[0], 'path': path}


    def __call__(self, method='GET'):
        uri = self._uri

        if method == 'GET':
            return self.fetch(uri=uri)
        if method == 'POST':
            return self.fetch(uri=uri, method='POST')

        return self

    async def fetch(self, uri, port=80, method='GET'):
        kwargs = self.uri_parse(uri)
        kwargs["method"] = method

        request_string = self._request_header % kwargs


        connect = asyncio.open_connection(uri, port)
        reader, writer = await connect

        writer.write(request_string.encode('utf-8'))

        await writer.drain()

        response_header = {}
        response_body = b''

        response_line = await reader.readline()

        first_header = response_line.rstrip()
        print(first_header)
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



if __name__ == '__main__':
    requests = HTTPRequest()

    loop = asyncio.get_event_loop()

    tasks = [requests.fetch("www.baidu.com", 443)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()