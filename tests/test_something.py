from assertpy import assert_that

from src.something import do_something


def test_do_something():
    assert_that(do_something()).is_equal_to(False)
