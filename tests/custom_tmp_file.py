# -*- coding: utf-8 -*-
"""Pytest fixtures.

Well, sort of.
Pytest does not allow for class based fixtures,
so the best alternative in this case is to create a module local to the tests
that can easily imported and used within them.

This module contains the code for a ``CustomTempFile`` class,
as well as several variables representing longer file contents needed in some tests.

Attributes
----------
BIOMART_RESPONSE : str
    Example response from a BioMart query, pre-processing.
BIOMART_CONTENTS : str
    Example response from a BioMart query, post-processing.
GTEX_CONTENTS : str
    Example response from a GTEx query.
MANE_CONTENTS : str
    Minimal MANE file contents.
"""

from __future__ import annotations

import os
from tempfile import NamedTemporaryFile
from types import TracebackType
from typing import Optional, Type

BIOMART_RESPONSE = """
HGNC symbol\tGene stable ID\tTranscript stable ID\tRefSeq mRNA ID
DLX1\tENSG00000144355\tENST00000341900\tNM_001038493
DLX1\tENSG00000144355\tENST00000361725\tNM_178120
DLX1\tENSG00000144355\tENST00000409492\t
DLX1\tENSG00000144355\tENST00000475989\t
DLX1\tENSG00000144355\tENST00000550686\t
DLX1\tENSG00000144355\tENST00000361609\t
"""


BIOMART_CONTENTS = """
geneSymbol,gencodeId,transcriptId,refseq
DLX1,ENSG00000144355,ENST00000341900,NM_001038493
DLX1,ENSG00000144355,ENST00000361725,NM_178120
DLX1,ENSG00000144355,ENST00000409492,
DLX1,ENSG00000144355,ENST00000475989,
DLX1,ENSG00000144355,ENST00000550686,
DLX1,ENSG00000144355,ENST00000361609,
"""

GTEX_RESPONSE = """
gencodeId\tgeneSymbol\ttissueSiteDetailId\ttranscriptId\tmedian\tunit\tdatasetId
ENSG00000144355.14\tDLX1\tBrain_Hypothalamus\tENST00000341900.6\t5.184999942779541\tread count\tgtex_v8
ENSG00000144355.14\tDLX1\tBrain_Hypothalamus\tENST00000361609.4\t0.23999999463558197\tread count\tgtex_v8
ENSG00000144355.14\tDLX1\tBrain_Hypothalamus\tENST00000361725.4\t3.1599998474121094\tread count\tgtex_v8
ENSG00000144355.14\tDLX1\tBrain_Hypothalamus\tENST00000409492.1\t1.2300000190734863\tread count\tgtex_v8
ENSG00000144355.14\tDLX1\tBrain_Hypothalamus\tENST00000469444.6\t0.0\tread count\tgtex_v8
ENSG00000144355.14\tDLX1\tBrain_Hypothalamus\tENST00000475989.2\t1.225000023841858\tread count\tgtex_v8
ENSG00000144355.14\tDLX1\tBrain_Hypothalamus\tENST00000550686.1\t0.4699999988079071\tread count\tgtex_v8
"""

GTEX_CONTENTS = """
gencodeId,geneSymbol,tissueSiteDetailId,transcriptId,median,unit,datasetId
ENSG00000144355,DLX1,Brain_Hypothalamus,ENST00000341900,5.184999942779541,read count,gtex_v8
ENSG00000144355,DLX1,Brain_Hypothalamus,ENST00000361725,3.1599998474121094,read count,gtex_v8
ENSG00000144355,DLX1,Brain_Hypothalamus,ENST00000409492,1.2300000190734863,read count,gtex_v8
ENSG00000144355,DLX1,Brain_Hypothalamus,ENST00000475989,1.225000023841858,read count,gtex_v8
ENSG00000144355,DLX1,Brain_Hypothalamus,ENST00000550686,0.4699999988079071,read count,gtex_v8
ENSG00000144355,DLX1,Brain_Hypothalamus,ENST00000361609,0.2399999946355819,read count,gtex_v8
"""

MANE_CONTENTS = (
    "#NCBI_GeneID,gencodeId,HGNC_ID,geneSymbol,name,refseq,RefSeq_prot,transcriptId,"
    "Ensembl_prot,MANE_status,GRCh38_chr,chr_start,chr_end,chr_strand\n"
    "GeneID:1745,ENSG00000144355,HGNC:2914,DLX1,distal-less homeobox 1,NM_178120,"
    "NP_835221.2,ENST00000361725,ENSP00000354478.4,MANE Select,2,172085507,172089674,+"
)


class CustomTempFile:
    """Create a temporary file with custom content.

    This is best used within a context manager to insure proper file clean up.

    Adapted from a StackOverflow `answer <https://stackoverflow.com/a/54053967>`_.

    Parameters
    ----------
    content : str
        Content of created temporary file.

    Examples
    --------
    >>> with CustomTempFile('Hello World') as tmp:
    >>>     with open(tmp.filename, 'r') as file:
    >>>         assert file.read() == 'Hello World'

    """

    def __init__(self, content: str) -> None:
        self.file = NamedTemporaryFile(mode="w", delete=False)
        with self.file as file:
            file.write(content)

    @property
    def filename(self) -> str:
        """Return the filename of the created file.

        Returns
        -------
        str
            The filename.
        """
        return self.file.name

    def __enter__(self) -> CustomTempFile:
        """Call on entry into ``with`` statement.

        Returns
        -------
        CustomTempFile
            Instance of self
        """
        return self

    def __exit__(
        self,
        ex_type: Optional[Type[BaseException]],
        ex_val: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        """Call on exit from with statement.

        Typing via `mypy`_.

        .. _mypy: https://github.com/python/mypy/issues/4885

        Parameters
        ----------
        ex_type : Optional[Type[BaseException]]
            Exception type
        ex_val : Optional[BaseException]
            Exception value
        tb : Optional[TracebackType]
            Traceback

        """
        os.unlink(self.filename)
