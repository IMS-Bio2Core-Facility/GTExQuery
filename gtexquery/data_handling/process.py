# -*- coding: utf-8 -*-
"""Data handling for *process* step."""

import logging
from pathlib import Path
from typing import Union

import pandas as pd

logger = logging.getLogger(__name__)


def merge_data(
    gtex_path: Union[Path, str],
    bm_path: Union[Path, str],
    mane: pd.DataFrame,
    out_path: Union[Path, str],
) -> None:
    """Merge the data from previous pipeline queries.

    Parameters
    ----------
    gtex_path : Union[Path, str]
        Path to the file containing GTEx query data.
    bm_path : Union[Path, str]
        Path to the file containing BioMart query data.
    mane : pd.DataFrame
        A DataFrame containing MANE annotations.
    out_path : Union[Path, str]
        Path to the output file.
    """
    gtex = pd.read_csv(gtex_path, header=0, index_col=None)

    gene = gtex["geneSymbol"].unique()[0]
    logger.info(f"Processing data for gene {gene}")

    bm = pd.read_csv(bm_path, header=0, index_col=None)
    data = (
        gtex.merge(bm, on=["geneSymbol", "gencodeId", "transcriptId"], how="outer")
        .merge(
            mane,
            on=["geneSymbol", "gencodeId", "transcriptId", "refseq"],
            how="left",
        )
        .sort_values(["median", "MANE_status"])
    )
    data.to_csv(out_path, index=False)
    logger.info(f"Gene {gene} processed!")
