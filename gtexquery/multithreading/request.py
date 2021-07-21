# -*- coding: utf-8 -*-
"""Functions for concurrent GTEx requests.

.. warning::

   Though every effort has been made to ensure thread safety,
   the concurrency is, as of yet, untested.

.. note::

   This module will likely undergo significant refactoring to generalise
   the concurrency pipeline and move all data handling code to a separate
   model.

Any API query is likely to be an I/O bound process,
particularly if there are many to make.
As this is a single step,
many in, many out process,
concurrency can be easily achieved with a thread local ``requests.session``
and mapping with ``concurrent.futures.ThreadPoolExecutor.map``.
The call to ``concurrent.futures.ThreadPoolExecutor.map`` is handled in the analysis
script.
"""
import logging
import threading
from typing import Optional

import requests

thread_local = threading.local()
logger = logging.getLogger(__name__)


def _get_session(
    headers: Optional[dict[str, str]] = None, params: Optional[dict[str, str]] = None
) -> requests.Session:
    """Instantiate a thread local session.

    The requests session is not thread safe,
    per `this thread <https://github.com/psf/requests/issues/2766>`_.
    To circumvent this, we create a thread local session. This means each session
    will still make multiple requests but remain isolated to its calling thread.

    Parameters
    ----------
    headers : Optional[dict[str, str]]
        Headers to be used for the session
    params : Optional[dict[str, str]]
        Parameters to be used for the session

    Returns
    -------
    requests.Session
    """
    # session still worth it - re-used by each thread
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
        if headers:
            thread_local.session.headers.update(headers)
        if params:
            thread_local.session.params.update(params)  # type: ignore
    return thread_local.session
