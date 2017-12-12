# python3 web server

用于学习研究HTTP协议与asyncio uvloop的使用

```python
from aquarius import Aquarius
from response import HTTPResponse

app = Aquarius(__name__)

@app.route("/")
async def test(request):
    return HTTPResponse(200)("aquarius")
```
![Image text](https://github.com/AquariusMr/aquarius/blob/master/img-test/test.png)