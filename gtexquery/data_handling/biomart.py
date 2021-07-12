# -*- coding: utf-8 -*-
"""Data handling for *biomart* step."""
import logging
import threading
from dataclasses import dataclass
from io import StringIO
from time import sleep

import pandas as pd
from bioservices import BioMart

thread_local = threading.local()
logger = logging.getLogger(__name__)


@dataclass()
class BMSession:
    """A pipeline for requesting multiple transcripts from BioMart.

    Parameters
    ----------
    transcripts : list[str]
        A list of *version-less* ENST IDs
    output : str
        Where to save the csv results file
    """

    transcripts: list[str]
    output: str

    def __post_init__(self) -> None:
        """Initialise thread local BioMart session."""
        self._s = self._get_biomart()

    def _get_biomart(self) -> BioMart:
        """Instantiate a thread local BioMart session.

        Returns
        -------
        BioMart

        """
        # session still worth it - re-used by each thread
        if not hasattr(thread_local, "bm"):
            thread_local.bm = BioMart(host="www.ensembl.org", verbose=False, cache=False)
            logger.info(f"Generated BioMart with host {thread_local.bm.host}")
        return thread_local.bm

    def _prepare_query(self, transcript: str) -> tuple[BioMart, str]:
        """Prepare a BioMart query.

        Using the thread_local session provided during post-initialisation,
        prepare a BioMart query by adding the appropriate attributes.

        Note
        ----
        Calling this will erase the attributes of any previous query.

        Parameters
        ----------
        transcript : str
            A *version-less* ENST ID

        Returns
        -------
        tuple[BioMart, str]
            A tuple consisting of the prepared, thread_local sesssion with the correct
            attributes and the xml content of the query.
        """
        self._s.new_query()
        self._s.add_dataset_to_xml("hsapiens_gene_ensembl")
        self._s.add_filter_to_xml("ensembl_transcript_id", transcript)
        self._s.add_attribute_to_xml("hgnc_symbol")
        self._s.add_attribute_to_xml("ensembl_gene_id")
        self._s.add_attribute_to_xml("ensembl_transcript_id")
        self._s.add_attribute_to_xml("refseq_mrna")
        xml = self._s.get_xml()
        return self._s, xml

    def _query_biomart(self, transcript: str) -> pd.DataFrame:
        """Reguest data on a transcript from BioMart.

        A thread-local session is provided during post-initialisation.

        With the BioMart interface, simultaneous requests for multiple transcripts only
        return data for the last transcript. Ergo, this function must be mapped over all
        input transcipts individually.

        Parameters
        ----------
        transcript : str
            A *version-less* ENST ID

        Returns
        -------
        pd.DataFrame
            Containing the geneSymbol, gencodeId, transcriptId, and refseq ID of the
            transcript. If refseq is NA, then there is no corresponding ID in BioMart.

        Raises
        ------
        TimeoutError
            When BioMart cannot be reached after 5 tries

        """
        s, xml = self._prepare_query(transcript)

        logger.info(f"Requesting transcript {transcript}")

        i = 0
        # Bioservices does not raise error, so we must check manually.
        # This can probably be improved...
        while "ERROR" in (message := s.query(xml)):
            logger.warning(f"Query error for {transcript}. Trying again in 0.1 s.")
            i += 1
            try:
                if i > 5:
                    raise TimeoutError
            except TimeoutError:
                logger.exception(
                    f"Query for {transcript} failed. Likely a BioMart connection issue."
                )
                raise
            else:
                sleep(0.1)
        else:
            data = pd.read_csv(
                StringIO(message),
                sep="\t",
                header=None,
                names=["geneSymbol", "gencodeId", "transcriptId", "refseq"],
            )
        return data

    def biomart_request(self) -> None:
        """Request data on multiple ENST IDs from BioMart."""
        data = pd.concat([self._query_biomart(t) for t in self.transcripts])
        data.to_csv(self.output, index=False)
        logger.info(f"Data saved to {self.output}")
