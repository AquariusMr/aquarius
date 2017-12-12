from aquarius import Aquarius
from response import HTTPResponse

app = Aquarius(__name__)


@app.route("/")
async def test(request):
    return HTTPResponse(200)("aquarius")

app.run(port=8000)
