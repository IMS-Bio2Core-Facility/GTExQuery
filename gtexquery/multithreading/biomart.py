# -*- coding: utf-8 -*-
"""Classes and functions for concurrent BioMart requests.

.. warning::

   Though every effort has been made to ensure thread safety,
   the concurrency is, as of yet, untested.

.. note::

   This module will likely undergo significant refactoring to generalise
   the concurrency pipeline and move all data handling code to a separate
   model.

Any API query is likely to be an I/O bound process,
particularly if there are many to make.
As this is a many in, many out process,
a call to ``concurrency.futures.ThreadPoolExecutor.map`` is sufficient,
though this call occurs in the analysis script.
"""
import logging
import threading

import requests

thread_local = threading.local()
logger = logging.getLogger(__name__)


def _get_session() -> requests.Session:
    """Instantiate a thread local session.

    The requests session is not thread safe,
    per `this thread <https://github.com/psf/requests/issues/2766>`_.
    To circumvent this, we create a thread local session. This means each session
    will still make multiple requests but remain isolated to its calling thread.

    Returns
    -------
    requests.Session
    """
    # session still worth it - re-used by each thread
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session
