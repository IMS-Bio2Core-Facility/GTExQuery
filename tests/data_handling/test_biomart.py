# -*- coding: utf-8 -*-
"""Tests for the scripts.data_handling.biomart submodule."""
from io import StringIO
from pathlib import Path

import pandas as pd
import pytest
import requests_mock
from pandas.testing import assert_frame_equal
from requests import HTTPError

from gtexquery.data_handling.biomart import XML_QUERY, biomart_request

from ..custom_tmp_file import (
    BIOMART_CONTENTS,
    BIOMART_RESPONSE,
    GTEX_CONTENTS,
    CustomTempFile,
)

transcripts = [
    "ENST00000341900",
    "ENST00000361725",
    "ENST00000409492",
    "ENST00000475989",
    "ENST00000550686",
    "ENST00000361609",
]


def test_raises_http_error(tmp_path: Path) -> None:
    """It raises an HTTPError."""
    with pytest.raises(HTTPError), requests_mock.Mocker() as m:
        m.get(
            "http://www.ensembl.org/biomart/martservice?query="
            + XML_QUERY(transcripts),
            status_code=400,
        )
        biomart_request(CustomTempFile(GTEX_CONTENTS).filename, str(tmp_path))


def test_writes_file(tmp_path: Path) -> None:
    """It writes the file."""
    with requests_mock.Mocker() as m:
        m.get(
            "http://www.ensembl.org/biomart/martservice?query="
            + XML_QUERY(transcripts),
            text=BIOMART_RESPONSE,
        )
        biomart_request(
            CustomTempFile(GTEX_CONTENTS).filename, str(tmp_path / "output.csv")
        )
    response = pd.read_csv(tmp_path / "output.csv")
    expected = pd.read_csv(StringIO(BIOMART_CONTENTS))
    assert_frame_equal(response, expected)
