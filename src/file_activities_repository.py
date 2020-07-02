import json
import os
from typing import List

from toolz import pipe
from toolz.curried import filter, map

from src.activities_repository import FindActivitiesCriteria


def fetch_activities_by_criteria_geojson(criteria: FindActivitiesCriteria) -> List[dict]:
    activities = read_file()

    filtered_activities = pipe(
        activities,
        filter(lambda activity: is_activity_satisfied_by_criteria(activity, criteria)),
        map(lambda activity: convert_activity_into_geojson(activity))
    )

    return list(filtered_activities)


def is_activity_satisfied_by_criteria(activity: dict, criteria: FindActivitiesCriteria) -> bool:
    return (filter_by_key(activity, 'category', criteria) and
            filter_by_key(activity, 'location', criteria) and
            filter_by_key(activity, 'district', criteria))


def filter_by_key(activity: dict, key: str, criteria: FindActivitiesCriteria):
    if not getattr(criteria, key):
        return True

    return activity[key] == getattr(criteria, key)


def convert_activity_into_geojson(activity: dict) -> dict:
    return {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': activity['latlng']
        },
        'properties': activity
    }


def read_file() -> List[dict]:
    with open(os.path.dirname(os.path.realpath(__file__)) + '/madrid.json') as f:
        data = json.load(f)

        return data
