# python3 web server;

```python3
    app = Aquarius(__name__)

    @app.route("/")
    def test(request):
        print(request.url)
        return json_response({"name": "shihongguang"})

    app.run()
```
