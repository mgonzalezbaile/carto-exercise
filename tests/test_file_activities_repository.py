from assertpy import assert_that

from src.activities_repository import FindActivitiesCriteria
from src.file_activities_repository import is_activity_satisfied_by_params, convert_activity_into_geojson, \
    fetch_activities_by_criteria_geojson, is_activity_satisfied_by_time_range, \
    fetch_recommended_activity_by_criteria_geojson


def test_should_satisfy_activity_by_simple_criteria():
    location = 'some location'
    activity = {'location': location}
    criteria = FindActivitiesCriteria(location=location)

    assert_that(is_activity_satisfied_by_params(activity, criteria)).is_true()


def test_should_not_satisfy_activity_by_simple_criteria():
    location = 'some location'
    activity = {'location': location}
    criteria = FindActivitiesCriteria(location='another location')

    assert_that(is_activity_satisfied_by_params(activity, criteria)).is_false()


def test_should_satisfy_activity_by_composed_criteria():
    location = 'some location'
    district = 'some district'

    activity = {'location': location, 'district': district}
    criteria = FindActivitiesCriteria(location=location, district=district)

    assert_that(is_activity_satisfied_by_params(activity, criteria)).is_true()


def test_should_not_satisfy_activity_by_composed_criteria():
    location = 'some location'
    district = 'some district'

    activity = {'location': location, 'district': 'another district'}
    criteria = FindActivitiesCriteria(location=location, district=district)

    assert_that(is_activity_satisfied_by_params(activity, criteria)).is_false()


def test_should_convert_activity_into_geojson():
    activity = {
        "name": "El Rastro",
        "opening_hours": {
            "mo": [],
            "tu": [],
            "we": [],
            "th": [],
            "fr": [],
            "sa": [],
            "su": ["09:00-15:00"]
        },
        "hours_spent": 2.5,
        "category": "shopping",
        "location": "outdoors",
        "district": "Centro",
        "latlng": [40.4087357, -3.7081466]
    }

    geojson_activity = convert_activity_into_geojson(activity)

    assert_that(geojson_activity).is_equal_to({
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [40.4087357, -3.7081466]
        },
        'properties': {
            "name": "El Rastro",
            "opening_hours": {
                "mo": [],
                "tu": [],
                "we": [],
                "th": [],
                "fr": [],
                "sa": [],
                "su": ["09:00-15:00"]
            },
            "hours_spent": 2.5,
            "category": "shopping",
            "location": "outdoors",
            "district": "Centro",
            "latlng": [40.4087357, -3.7081466]
        }
    })


def test_should_fetch_activities_by_criteria_in_geojson_format():
    geojson_activities = fetch_activities_by_criteria_geojson(FindActivitiesCriteria(
        location='outdoors',
        district='Centro',
        category='shopping'
    ))

    assert_that(geojson_activities).is_equal_to({
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [40.4087357, -3.7081466]
                },
                'properties': {
                    'name': 'El Rastro',
                    'opening_hours': {'mo': [], 'tu': [], 'we': [], 'th': [], 'fr': [], 'sa': [],
                                      'su': ['09:00-15:00']},
                    'hours_spent': 2.5,
                    'category': 'shopping',
                    'location': 'outdoors',
                    'district': 'Centro',
                    'latlng': [40.4087357, -3.7081466]
                }
            },
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [40.4199837, -3.7054455]
                },
                'properties': {
                    'name': 'Gran Vía',
                    'opening_hours': {'mo': ['00:00-23:59'], 'tu': ['00:00-23:59'], 'we': ['00:00-23:59'],
                                      'th': ['00:00-23:59'], 'fr': ['00:00-23:59'], 'sa': ['00:00-23:59'],
                                      'su': ['00:00-23:59']},
                    'hours_spent': 1,
                    'category': 'shopping',
                    'location': 'outdoors',
                    'district': 'Centro',
                    'latlng': [40.4199837, -3.7054455]
                }
            }
        ]
    })


def test_should_satisfy_activity_by_hours_spent():
    activity = {"hours_spent": 1, "opening_hours": {"mo": ["00:00-23:59"]}}

    criteria = FindActivitiesCriteria(
        from_time='11:00',
        to_time='12:00'
    )

    assert_that(is_activity_satisfied_by_time_range(activity, criteria)).is_true()

    criteria = FindActivitiesCriteria(
        from_time='11:10',
        to_time='12:15'
    )

    assert_that(is_activity_satisfied_by_time_range(activity, criteria)).is_true()


def test_should_not_satisfy_activity_by_hours_spent():
    activity = {"hours_spent": 1, "opening_hours": {"mo": ["00:00-23:59"]}}

    criteria = FindActivitiesCriteria(
        from_time='11:00',
        to_time='11:30'
    )

    assert_that(is_activity_satisfied_by_time_range(activity, criteria)).is_false()

    criteria = FindActivitiesCriteria(
        from_time='11:00',
        to_time='11:59'
    )

    assert_that(is_activity_satisfied_by_time_range(activity, criteria)).is_false()


def test_should_satisfy_activity_by_time_range_criteria():
    activity = {
        "opening_hours": {
            "mo": ["00:00-06:00"],
            "tu": ["00:00-23:59"],
            "we": ["00:00-23:59"],
            "th": ["00:00-23:59"],
            "fr": ["00:00-23:59"],
            "sa": ["00:00-23:59"],
            "su": ["00:00-23:59"]
        },
        "hours_spent": 1,
    }

    criteria = FindActivitiesCriteria(
        from_time='11:00',
        to_time='12:30'
    )

    assert_that(is_activity_satisfied_by_time_range(activity, criteria)).is_true()

    criteria = FindActivitiesCriteria(
        from_time='00:01',
        to_time='23:58'
    )

    assert_that(is_activity_satisfied_by_time_range(activity, criteria)).is_true()


def test_should_not_satisfy_activity_by_time_range_criteria():
    activity = {
        "opening_hours": {
            "mo": ["00:00-06:00"],
            "tu": ["10:00-12:00"],
            "we": [],
            "th": [],
            "fr": [],
            "sa": [],
            "su": []
        },
        "hours_spent": 1,
    }

    criteria = FindActivitiesCriteria(
        from_time='10:15',
        to_time='12:30'
    )

    assert_that(is_activity_satisfied_by_time_range(activity, criteria)).is_false()


def test_should_recommend_activity():
    criteria = FindActivitiesCriteria(
        category='shopping',
        from_time='09:30',
        to_time='14:30'
    )

    recommended_activity = fetch_recommended_activity_by_criteria_geojson(criteria)
    assert_that(recommended_activity['properties']['name']).is_equal_to('El Rastro')

    criteria = FindActivitiesCriteria(
        category='shopping',
        from_time='16:30',
        to_time='20:30'
    )

    recommended_activity = fetch_recommended_activity_by_criteria_geojson(criteria)
    assert_that(recommended_activity['properties']['name']).is_equal_to('ECI Nuevos Ministerios')
