import json
import os
import pathlib
from typing import List

from flask import Response, Flask, request
from toolz import pipe
from toolz.curried import filter

app = Flask(__name__)


@app.route('/activities', methods=['GET'])
def get_activities():
    activities = read_file()
    filtered_activities = pipe(
        activities,
        filter_by_query_params(request.args)
    )

    result = {"text": "hello World"}

    return Response(response=json.dumps(activities), headers={'Content-Type': 'application/json'})


def read_file() -> List[dict]:
    with open(os.path.dirname(os.path.realpath(__file__)) + '/madrid.json') as f:
        data = json.load(f)

        return data


def find_activities_by_criteria(criteria):
    activities = read_file()
    filtered_activities = pipe(
        activities,
        filter_by_query_params(criteria)
    )

    return list(filtered_activities)


def filter_by_query_params(query_params: dict) -> callable:
    if not query_params:
        return lambda activity: activity

    return filter(
        lambda activity:
        filter_by_key(activity, 'category', query_params) or
        filter_by_key(activity, 'location', query_params) or
        filter_by_key(activity, 'district', query_params)
    )


def filter_by_key(activity, key, query_params):
    return (key in query_params) and (activity[key] == query_params[key])
