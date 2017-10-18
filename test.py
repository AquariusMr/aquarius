from sanic import Sanic
from sanic.response import json


app = Sanic()

@app.route("/")
async def test(request):
    return json({"hello": "world"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=False)



https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx9aac9c21368447e6&redirect_uri=https%3a%2f%2ftest.xinlianxd.com%2f&response_type=code&scope=snsapi_base&state=123#wechat_redirect

462a3ca630034191f0a5faacd75aa60f