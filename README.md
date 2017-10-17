# python3 web server


```python
from app import Aquarius
from fetch import HTTPRequest


app = Aquarius(__name__)


@app.route("/")
async def test(request):
    result = await app.exec_task(HTTPRequest().get("www.baidu.com"))
    return HttpResponse.set_cookie("name", "shihongguang")(result)

app.run()
```
