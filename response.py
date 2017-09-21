try:
    import ujson as json
except ImportError:
    import json


def json_response(struct):
    body = json.dumps(struct)

    t = [
        b'HTTP/1.1 200 OK',
        b'Content-Type:application/json; charset=utf-8',
        b'',
        b'',
        b'\r\n']

    t[-2] = bytes(body, encoding='utf-8')
    t[-3] = bytes('Content-Length:'+str(len(body)+4) + "\r\n", encoding='utf-8')

    return b'\r\n'.join(t)