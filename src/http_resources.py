import json
import os

from flask import Response, Flask, request

from src.activities_repository import FindActivitiesCriteria, ActivitiesRepository
from src.file_activities_repository import FileActivitiesRepository

app = Flask(__name__)


@app.route('/activities', methods=['GET'])
def get_activities():
    result = activities_repository().fetch_activities_by_criteria_geojson(FindActivitiesCriteria(
        location=request.args.get('location', None),
        district=request.args.get('district', None),
        category=request.args.get('category', None),
    ))

    return Response(response=json.dumps(result), headers={'Content-Type': 'application/json'})


@app.route('/recommendation', methods=['GET'])
def get_recommendations():
    if not request.args.get('category') or not request.args.get('from_time') or not request.args.get('to_time'):
        return Response(status=422)

    result = activities_repository().fetch_recommended_activity_by_criteria_geojson(FindActivitiesCriteria(
        category=request.args.get('category'),
        from_time=request.args.get('from_time'),
        to_time=request.args.get('to_time'),
    ))

    return Response(response=json.dumps(result), headers={'Content-Type': 'application/json'})


def activities_repository() -> ActivitiesRepository:
    return FileActivitiesRepository(os.path.dirname(os.path.realpath(__file__)) + '/madrid.json')
