# python3 web server;

```python
from app import Aquarius


app = Aquarius(__name__)

@app.route("/")
def test(request):
    print(request.url)
    return {"name": "shihongguang"}

app.run()
```
