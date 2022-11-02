import json

import pytest

import checkLogsExist.hello_world.app as app


def test_get_end_time():
    end_time = app.get_end_time("22-45", "10")
    assert end_time == "22-55"


def test_get_end_time_edge():
    end_time = app.get_end_time("22-55", "10")
    assert end_time == "23-05"
