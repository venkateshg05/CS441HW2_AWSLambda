import json

import pytest

import getLogs.hello_world.app as app


def test_get_log_file_idx():
    timestamps = ["22-41", "22-42", "22-43", "22-44", "22-45", "22-46"]
    log_file_idx = app.get_log_file_idx(
        0, len(timestamps)-1, "22-45", timestamps)
    assert log_file_idx == 4


def test_get_log_file_idx_edge():
    timestamps = ["22-41", "22-42", "22-43", "22-44", "22-45", "22-46"]
    log_file_idx = app.get_log_file_idx(
        0, len(timestamps)-1, "22-41", timestamps)
    assert log_file_idx == 0


def test_get_log_file_idx_invalid():
    timestamps = ["22-41", "22-42", "22-43", "22-44", "22-45", "22-46"]
    log_file_idx = app.get_log_file_idx(
        0, len(timestamps)-1, "22-50", timestamps)
    assert log_file_idx == "Not found"
