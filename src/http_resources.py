import json

from flask import Response, Flask

app = Flask(__name__)


@app.route('/activities', methods=['GET'])
def get_activities():
    result = {"text": "hello World"}

    return Response(response=json.dumps(dict(result)), headers={'Content-Type': 'application/json'})
