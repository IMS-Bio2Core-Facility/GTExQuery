# -*- coding: utf-8 -*-
"""Tests for the multithreading.biomart submodule."""
import requests

from gtexquery.multithreading.biomart import _get_session, thread_local


def test_has_attr() -> None:
    """It gives thread local a sesson attribute."""
    _ = _get_session()
    assert hasattr(thread_local, "session"), "There is no session attribute."


def test_has_session() -> None:
    """It returns a session."""
    s = _get_session()
    assert isinstance(s, requests.Session), "It does not return a session."
