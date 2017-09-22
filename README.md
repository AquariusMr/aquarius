# python3 web server;

```python
from app import Aquarius


app = Aquarius(__name__)

@app.route("/")
def test(request):
    print(request.url)
    return json_response({"name": "shihongguang"})

app.run()
```
