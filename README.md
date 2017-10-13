# python3 web server;

```python
from app import Aquarius


app = Aquarius(__name__)


@app.route("/")
async def test(request):
	return HttpResponse.set_cookie("name", "shihongguang")("Aquarius")

app.run()
```
