import json
from typing import List

import arrow
from toolz import pipe
from toolz.curried import filter, map

from src.activities_repository import FindActivitiesCriteria, ActivitiesRepository


class FileActivitiesRepository(ActivitiesRepository):
    def __init__(self, filepath):
        self.filepath = filepath

    def fetch_activities_by_criteria_geojson(self, criteria: FindActivitiesCriteria) -> dict:
        activities = self._read_file()

        filtered_activities = pipe(
            activities,
            filter(lambda activity: self._is_activity_satisfied_by_params(activity, criteria)),
            map(lambda activity: self._convert_activity_into_geojson(activity))
        )

        return {
            'type': 'FeatureCollection',
            'features': list(filtered_activities)
        }

    def fetch_recommended_activity_by_criteria_geojson(self, criteria: FindActivitiesCriteria) -> dict:
        activities = self._read_file()

        filtered_activities = pipe(
            activities,
            filter(lambda activity: self._is_activity_satisfied_by_params(activity, criteria)),
            filter(lambda activity: self._is_activity_satisfied_by_time_range(activity, criteria)),
            map(lambda activity: self._convert_activity_into_geojson(activity))
        )

        longest_visit_time = 0
        longest_visit_time_activity = {}
        for activity in filtered_activities:
            if activity['properties']['hours_spent'] > longest_visit_time:
                longest_visit_time = activity['properties']['hours_spent']
                longest_visit_time_activity = activity

        return longest_visit_time_activity

    def _is_activity_satisfied_by_params(self, activity: dict, criteria: FindActivitiesCriteria) -> bool:
        return (self._is_activity_satisfied_by_value(activity, 'category', criteria) and
                self._is_activity_satisfied_by_value(activity, 'location', criteria) and
                self._is_activity_satisfied_by_value(activity, 'district', criteria))

    def _is_activity_satisfied_by_value(self, activity: dict, key: str, criteria: FindActivitiesCriteria) -> bool:
        if not getattr(criteria, key):
            return True

        return activity[key] == getattr(criteria, key)

    def _is_activity_satisfied_by_time_range(self, activity: dict, criteria: FindActivitiesCriteria) -> bool:
        now = arrow.now()
        visit_from_time = now.replace(hour=int(criteria.from_time.split(':')[0]), minute=int(criteria.from_time.split(':')[1]), second=0)
        visit_to_time = now.replace(hour=int(criteria.to_time.split(':')[0]), minute=int(criteria.to_time.split(':')[1]), second=0)

        visit_hours = divmod((visit_to_time - visit_from_time).seconds, 3600)[0]

        if visit_hours < activity['hours_spent']:
            return False

        for day, opening_hours in activity['opening_hours'].items():
            if not opening_hours:
                continue
            from_opening_hour = opening_hours[0].split('-')[0]
            to_opening_hour = opening_hours[0].split('-')[1]
            from_opening_time = now.replace(hour=int(from_opening_hour.split(':')[0]), minute=int(from_opening_hour.split(':')[1]), second=0)
            to_opening_time = now.replace(hour=int(to_opening_hour.split(':')[0]), minute=int(to_opening_hour.split(':')[1]), second=0)
            if visit_from_time.is_between(from_opening_time, to_opening_time) and visit_to_time.is_between(from_opening_time, to_opening_time):
                return True

        return False

    def _convert_activity_into_geojson(self, activity: dict) -> dict:
        return {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': activity['latlng']
            },
            'properties': activity
        }

    def _read_file(self) -> List[dict]:
        with open(self.filepath) as f:
            data = json.load(f)

            return data
