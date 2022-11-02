import json

import pytest

import checkReqWithinBounds.check_req_within_bounds.app as app


def test_get_end_time():
    end_time = app.get_end_time("22-45", "10")
    assert end_time == "22-55"


def test_get_end_time_edge():
    end_time = app.get_end_time("22-55", "10")
    assert end_time == "23-05"
