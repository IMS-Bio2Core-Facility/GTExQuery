# -*- coding: utf-8 -*-
"""Data handling for *biomart* step.

Attributes
----------
XML_QUERY : Callable[[list[str]], str]
    A lambda funcion encapsulating the unwieldy XML query string required by
    Biomart. The list of transcript are joined to form the ensembl_transcript_id
    field.
"""
import logging
from io import StringIO
from typing import Callable

import pandas as pd
import requests

from ..multithreading.request import _get_session

logger = logging.getLogger(__name__)

XML_QUERY: Callable[[list[str]], str] = lambda transcripts: (
    "<?xml version='1.0' encoding='UTF-8'?>"
    "<!DOCTYPE Query>"
    "<Query  virtualSchemaName = 'default' formatter = 'TSV' header = '1'"
    " uniqueRows = '0' count = '' datasetConfigVersion = '0.6' >"
    "<Dataset name = 'hsapiens_gene_ensembl' interface = 'default' >"
    f"<Filter name = 'ensembl_transcript_id' value = '{','.join(transcripts)}'/>"
    "<Attribute name = 'hgnc_symbol' />"
    "<Attribute name = 'ensembl_gene_id' />"
    "<Attribute name = 'ensembl_transcript_id' />"
    "<Attribute name = 'refseq_mrna' />"
    "</Dataset>"
    "</Query>"
)


def biomart_request(infile: str, output: str) -> None:
    """Query Biomart with a list of transcripts.

    Instantiates a thread_local `request.Session` before querying Biomart
    with a list of transcript IDs. Should an error occur, it is logged using the
    `logging.exception` method.

    Parameters
    ----------
    infile : str
        The input file.
        This is expected to be the output of the GTEx query, and will fail if
        the expected columns are not present.
    output : str
        Where to save results

    Raises
    ------
    requests.HTTPError
        When the GET request fails
    """
    transcripts = pd.read_csv(infile)["transcriptId"].tolist()

    s = _get_session()
    response = s.get(
        "http://www.ensembl.org/biomart/martservice?query=" + XML_QUERY(transcripts)
    )

    try:
        response.raise_for_status()
    except requests.HTTPError:
        logger.exception(
            f"An error occurred while requesting {transcripts}. A detailed report follows"
        )
        raise
    else:
        logger.info(f"GET request for {transcripts} successful!")
        data = pd.read_csv(StringIO(response.text), sep="\t")
        data.columns = ["geneSymbol", "gencodeId", "transcriptId", "refseq"]
        data.to_csv(output, index=False)
