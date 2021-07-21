# -*- coding: utf-8 -*-
"""Data handling for *request* step."""
import contextlib
import csv
import logging
from io import StringIO
from typing import Optional

import pandas as pd
import requests

from ..multithreading.request import _get_session

logger = logging.getLogger(__name__)


def lut_check(gene: str, lut: pd.DataFrame) -> Optional[str]:  # type: ignore
    """Check that a gene is found in the Gencode annotations.

    If the gene is found, then it is converted to its Ensembl ID.
    If it is not found, then None is returned to signal to downstream processing
    that the gene is not in Gencode.

    `contextlib suppress <https://docs.python.org/3/library/contextlib.html>`_
    is used rather than the more verbose ``try/except``
    as we are only interested in returning ``none`` for this specific case.
    Any and all other cases should fail fast and hard.

    Note
    ----
    It's likely that your gene is in Gencode even if it is not found.
    Common reasons (at least for me!) that a gene might not be found include
    spelling errors and name errors (ie. using NGN2 instead of NEUROG2).

    Parameters
    ----------
    gene : str
        The gene name to be queried
    lut : pd.DataFrame
        The dataframe containing the name-to-id conversion for the genes

    Returns
    -------
    Optional[str]

    Example
    -------
    >>> lut = pd.DataFrame.from_dict({"name": ["ASCL1"], "id": ["ENSG00000139352.3"]})
    >>> lut_check("ASCL1", lut)
    'ENSG00000139352.3'
    >>> lut_check("NotAGene", lut)

    """
    with contextlib.suppress(IndexError):
        return lut.loc[lut["name"] == gene, "id"].values[0]


def gtex_request(region: str, gene: str, output: str) -> None:
    """Make a thead-safe gtex request against mediantranscriptexpression.

    If gene is a str, then a query is made to gtex; however, if gene is none, then
    a blank file is created and no query is performed.

    A thread local session is provided by a call to ``_get_session``.
    This allows the reuse of sessions, which, among other things,
    provides significant speed ups.

    Parameters
    ----------
    region : str
        The gtex region to query.
    gene : str
        The ensg to query.
    output : str
        Where to save the output file.

    Raises
    ------
    requests.HTTPError
        When the get request returns an error
    """
    # if gene is none, write blank file
    if gene is None:
        with open(output, "w") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "gencodeId",
                    "geneSymbol",
                    "tissueSiteDetailId",
                    "transcriptId",
                    "median",
                    "unit",
                    "datasetId",
                ]
            )
            logger.warning(
                "A gene was not found in gencode. An empty file has been created."
            )
            exit()

    s = _get_session(
        headers={"Accept": "text/html"},
        params={"datasetId": "gtex_v8", "tissueSiteDetailId": region, "format": "tsv"},
    )

    response = s.get(
        "https://gtexportal.org/rest/v1/expression/mediantranscriptexpression",
        params={
            "gencodeId": gene,
        },
    )

    try:
        response.raise_for_status()
    except requests.HTTPError:
        logger.exception(
            f"An error occurred while requesting {gene}. A detailed report follows..."
        )
        raise
    else:
        logger.info(f"Get request for {gene} successful!")
        data = pd.read_csv(StringIO(response.text), sep="\t")
        data = data.loc[data["median"] > 0, :].sort_values("median", ascending=False)
        data.loc[:, ["gencodeId", "transcriptId"]] = data.loc[
            :, ["gencodeId", "transcriptId"]
        ].apply(lambda x: x.str.split(".").str.get(0))
        data.to_csv(output, index=False)
