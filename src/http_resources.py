import json
import os
from dataclasses import dataclass
from typing import List, Optional

from flask import Response, Flask, request
from toolz import pipe
from toolz.curried import filter

app = Flask(__name__)


@dataclass
class FindActivitiesCriteria:
    category: Optional[str] = None
    location: Optional[str] = None
    district: Optional[str] = None


@app.route('/activities', methods=['GET'])
def get_activities():
    activities = read_file()
    filtered_activities = pipe(
        activities,
        filter_by_criteria(request.args)
    )

    result = {"text": "hello World"}

    return Response(response=json.dumps(activities), headers={'Content-Type': 'application/json'})


def read_file() -> List[dict]:
    with open(os.path.dirname(os.path.realpath(__file__)) + '/madrid.json') as f:
        data = json.load(f)

        return data


def find_activities_by_criteria(criteria: FindActivitiesCriteria):
    activities = read_file()
    filtered_activities = pipe(
        activities,
        filter_by_criteria(criteria)
    )

    return list(filtered_activities)


def filter_by_criteria(criteria: FindActivitiesCriteria) -> callable:
    return filter(
        lambda activity:
        filter_by_key(activity, 'category', criteria) and
        filter_by_key(activity, 'location', criteria) and
        filter_by_key(activity, 'district', criteria)
    )


def filter_by_key(activity, key, criteria: FindActivitiesCriteria):
    if not getattr(criteria, key):
        return True

    return hasattr(criteria, key) and (activity[key] == getattr(criteria, key))
