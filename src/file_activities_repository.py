import json
import os
from typing import List

import arrow
from toolz import pipe
from toolz.curried import filter, map

from src.activities_repository import FindActivitiesCriteria


def fetch_activities_by_criteria_geojson(criteria: FindActivitiesCriteria) -> dict:
    activities = read_file()

    filtered_activities = pipe(
        activities,
        filter(lambda activity: is_activity_satisfied_by_criteria(activity, criteria)),
        map(lambda activity: convert_activity_into_geojson(activity))
    )

    return {
        'type': 'FeatureCollection',
        'features': list(filtered_activities)
    }


def is_activity_satisfied_by_criteria(activity: dict, criteria: FindActivitiesCriteria) -> bool:
    return (is_activity_satisfied_by_value(activity, 'category', criteria) and
            is_activity_satisfied_by_value(activity, 'location', criteria) and
            is_activity_satisfied_by_value(activity, 'district', criteria))


def is_activity_satisfied_by_value(activity: dict, key: str, criteria: FindActivitiesCriteria) -> bool:
    if not getattr(criteria, key):
        return True

    return activity[key] == getattr(criteria, key)


def is_activity_satisfied_by_time_range(activity: dict, criteria: FindActivitiesCriteria) -> bool:
    now = arrow.now()
    from_time = now.replace(hour=int(criteria.from_time.split(':')[0]), minute=int(criteria.from_time.split(':')[1]), second=0)
    to_time = now.replace(hour=int(criteria.to_time.split(':')[0]), minute=int(criteria.to_time.split(':')[1]), second=0)

    visit_hours = divmod((to_time - from_time).seconds, 3600)[0]

    if visit_hours < activity['hours_spent']:
        return False

    return True


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
