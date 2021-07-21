# -*- coding: utf-8 -*-
"""Tests for the multithreading.biomart submodule.

As a thread_local request session is used, and a new session returned only if
thread_local does not have one, the thread_local session must be deleted at
the start of each test if we are to test initialisation of the Session. We can
easily test that the session is only created by calling the method twice with
different parameters and testing that the session has the parameters from the
first call.
"""
import requests

from gtexquery.multithreading.request import _get_session, thread_local


def test_has_attr() -> None:
    """It gives thread local a session attribute."""
    if hasattr(thread_local, "session"):
        del thread_local.session
    _ = _get_session()
    assert hasattr(thread_local, "session"), "There is no session attribute."


def test_returns_existing() -> None:
    """It returns an existing thread_local session."""
    if hasattr(thread_local, "session"):
        del thread_local.session
    s = _get_session()
    t = _get_session(headers={"phony": "phony"}, params={"phony": "phony"})
    assert s is t, "The original session was not returned."
    assert s.params == {}, "The session has parameters."
    assert (
        s.headers == requests.Session().headers
    ), "The session does not have default headers."


def test_has_session() -> None:
    """It returns a session."""
    if hasattr(thread_local, "session"):
        del thread_local.session
    s = _get_session()
    assert isinstance(s, requests.Session), "It does not return a session."


def test_clean_session() -> None:
    """The session does change the default headers/params, if none are passed."""
    if hasattr(thread_local, "session"):
        del thread_local.session
    s = _get_session()
    assert s.params == {}, "The session has parameters."
    assert (
        s.headers == requests.Session().headers
    ), "The session does not have default headers."


def test_updates_headers() -> None:
    """It updates the headers."""
    if hasattr(thread_local, "session"):
        del thread_local.session
    s = _get_session(headers={"Accept": "text/html", "phony": "phony"})
    expected = requests.Session().headers
    expected.update({"Accept": "text/html", "phony": "phony"})
    assert s.headers == expected, "The headers were not updated correctly."


def test_updates_params() -> None:
    """It updates the params."""
    if hasattr(thread_local, "session"):
        del thread_local.session
    s = _get_session(params={"phony": "phony"})
    assert s.params == {"phony": "phony"}
