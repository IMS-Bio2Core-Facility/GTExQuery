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

To simplify the multi-step process for mapping,
and allow for multiple transcripts to be queried,
a ``BMSession`` class is provided.
"""
import logging
import threading

import pandas as pd

from ..data_handling.biomart import BMSession

thread_local = threading.local()
logger = logging.getLogger(__name__)


def concurrent_biomart(file: str, output: str) -> None:
    """Given an input file, extract the ENST IDs and query BioMart.

    Note
    ----
    For use with ``concurrency.futures.ThreadPoolExecutor.map``.

    This is designed to allow concurrency within the given pipeline,
    as reading files and querying an external API are inherently I/O
    bound processes. Given the nature of this pipeline, the function
    expects the input file to contain a column `transcriptId` that
    contains a list of *version-less* ENST IDs from GTEx.

    Parameters
    ----------
    file : str
        Where to read the data from
    output : str
        Where to write the results to

    Raises
    ------
    IndexError
        If there are no transcipts to process in ``file``
    """
    logger.info(f"Processing file {file}")
    df = pd.read_csv(file, index_col=None)
    if len(transcripts := df.loc[:, "transcriptId"].unique().tolist()) == 0:
        logging.error(f"There are no transcripts for {file}. Raising index error")
        raise IndexError
    s = BMSession(transcripts, output)
    s.biomart_request()
