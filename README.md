# python3 web server


```python
	
	# 1.异步请求
	# 2.数据库缓存
	# 3.异步延迟调用	

    from already_sql import *
    from response import HttpResponse
    from fetch import HTTPRequest


    app_sql = MysqlAlready("127.0.0.1", "root", "mysql", "test")

    app = Aquarius(__name__)

    @app.route("/")
    async def index(request):
        result = await app.exec_task(HTTPRequest("www.baidu.com")("GET"))

        @app.awaiting(3)
        def printf(name):
            print(name)

        await printf("shihongguang")

        return HttpResponse.set_cookie("name", "shihongguang")(result)

    app.run()
```
