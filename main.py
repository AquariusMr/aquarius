from app import Aquarius
from response import json_response


app = Aquarius(__name__)


@app.route("/")
def test1(request):
    return json_response({"n": "s"})


app.run(port=8002, host="0.0.0.0")
