import json

from flask import Response, Flask, request

from src.activities_repository import FindActivitiesCriteria
from src.file_activities_repository import fetch_activities_by_criteria_geojson

app = Flask(__name__)


@app.route('/activities', methods=['GET'])
def get_activities():
    result = fetch_activities_by_criteria_geojson(FindActivitiesCriteria(
        location=request.args.get('location', None),
        district=request.args.get('district', None),
        category=request.args.get('category', None),
    ))

    return Response(response=json.dumps(result), headers={'Content-Type': 'application/json'})


@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    result = {}

    return Response(response=json.dumps(result), headers={'Content-Type': 'application/json'})
