import asyncio


async def fetch_test(host, port=80):

    headers = []
    body = b''

    print('request %s...' % host)

    connect = asyncio.open_connection(host, port)

    reader, writer = await connect

    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host

    writer.write(header.encode('utf-8'))

    await writer.drain()

    line = await reader.readline()
    agreement = line.rstrip()

    while True:
        line = await reader.readline()

        if line == b"\r\n":
            break
        headers.append(line.rstrip())

    while True:
        line = await reader.readline()

        if line == b"\r\n":
            break

        if line == b'':
            break

        body = body + line 

    writer.close()

    text = (agreement, headers, body)

    print(text)
    return text



if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    tasks = [fetch_test('0.0.0.0', 8002)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()