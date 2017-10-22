# python3 web server


```python

    from already_sql import *
    from response import HttpResponse
    from fetch import HTTPRequest


    app_sql = MysqlAlready("127.0.0.1", "root", "mysql", "test")

    app = Aquarius(__name__)

    # 支持异步请求,延迟调用
    @app.route("/")
    async def index(request):
        result = await app.exec_task(HTTPRequest("www.baidu.com")("GET"))

        @app.awaiting(3)
        def printf(name):
            print(name)

        await printf("shihongguang")

        return HttpResponse.set_cookie("name", "shihongguang")(result)

    # 路由支持正则
    @app.route("/view(\d)(\d)")
    class View(app.View):

        def get(self, idt, pk):
            print(idt, pk)
            return HttpResponse("view hello")


    app.run()

    app.run()
```
