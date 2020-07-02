from assertpy import assert_that

from src.http_resources import find_activities_by_criteria, FindActivitiesCriteria
from src.something import do_something


def test_do_something():
    assert_that(do_something()).is_equal_to(False)


def test_find_activities_by_location():
    activities = find_activities_by_criteria(FindActivitiesCriteria(
        location='outdoors',
    ))

    assert_that(len(activities)).is_equal_to(7)

    for activity in activities:
        assert_that(activity['location'] == 'outdoors').is_true()

    activities = find_activities_by_criteria(FindActivitiesCriteria(
        location='indoors',
    ))

    assert_that(len(activities)).is_equal_to(3)

    for activity in activities:
        assert_that(activity['location'] == 'indoors').is_true()


def test_find_activities_by_criteria():
    activities = find_activities_by_criteria(FindActivitiesCriteria(
        location='outdoors',
        district='Centro'
    ))

    assert_that(len(activities)).is_equal_to(3)

    for activity in activities:
        assert_that(activity['location'] == 'outdoors').is_true()
        assert_that(activity['district'] == 'Centro').is_true()

    activities = find_activities_by_criteria(FindActivitiesCriteria(
        location='outdoors',
        district='Centro',
        category='shopping'
    ))

    assert_that(len(activities)).is_equal_to(2)

    for activity in activities:
        assert_that(activity['location'] == 'outdoors').is_true()
        assert_that(activity['district'] == 'Centro').is_true()
        assert_that(activity['category'] == 'shopping').is_true()
