# -*- coding: utf-8 -*-
"""Tests for the scripts.data_handling.process submodule.

These unit tests are designed to test that the results of the query
are handled correctly.
They assume the data returned by the API query is formatted correctly,
as tests of data returned by realworld API queries are best left to integrations tests.
As such,
representative data is included in the tests.data module.

Attributes
----------
MANE : pd.DataFrame
    A minimal MANE dataset
"""
from io import StringIO
from pathlib import Path

import pandas as pd

from gtexquery.data_handling.process import merge_data

from ..custom_tmp_file import (
    BIOMART_CONTENTS,
    GTEX_CONTENTS,
    MANE_CONTENTS,
    CustomTempFile,
)

MANE: pd.DataFrame = pd.read_csv(StringIO(MANE_CONTENTS))


def test_writes_file(tmp_path: Path) -> None:
    """It writes a file."""
    out_path = tmp_path / "out.csv"
    merge_data(
        CustomTempFile(GTEX_CONTENTS).filename,
        CustomTempFile(BIOMART_CONTENTS).filename,
        MANE,
        out_path,
    )
    assert out_path.stat().st_size > 0


def test_results_columns(tmp_path: Path) -> None:
    """Its columns are named correctly ."""
    columns = [
        "gencodeId",
        "geneSymbol",
        "tissueSiteDetailId",
        "transcriptId",
        "median",
        "unit",
        "datasetId",
        "refseq",
        "#NCBI_GeneID",
        "HGNC_ID",
        "name",
        "RefSeq_prot",
        "Ensembl_prot",
        "MANE_status",
        "GRCh38_chr",
        "chr_start",
        "chr_end",
        "chr_strand",
    ]
    out_path = tmp_path / "out.csv"
    merge_data(
        CustomTempFile(GTEX_CONTENTS).filename,
        CustomTempFile(BIOMART_CONTENTS).filename,
        MANE,
        out_path,
    )
    results = pd.read_csv(out_path, index_col=None)
    assert all(x in columns for x in results.columns), "Found an unexpected column."
    assert len(results.columns) == len(
        columns
    ), f"There should be {len(columns)} columns"


def test_sorted_results(tmp_path: Path) -> None:
    """The results are sorted by median.

    As the ``merge_data`` function technically sorts on "MANE_status" as well,
    it would be ideal to test that sort, too.
    However, it it impossible to know in advance how many will have this status,
    so we cannot check count.
    Additionally, we cannot check the sort as most values are NaN,
    and knowing the correct order would require prior knowledge about the number
    of GTEx transcripts and the number with MANE status.

    Parameters
    ----------
    tmp_path : Path
        pytest fixture for temporary path
    """
    out_path = tmp_path / "out.csv"
    merge_data(
        CustomTempFile(GTEX_CONTENTS).filename,
        CustomTempFile(BIOMART_CONTENTS).filename,
        MANE,
        out_path,
    )
    results = pd.read_csv(out_path, index_col=None)
    assert results["median"].is_monotonic
