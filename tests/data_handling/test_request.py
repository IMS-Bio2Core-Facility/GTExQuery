# -*- coding: utf-8 -*-
"""Tests for the scripts.data_handling.request submodule.

These unit tests are designed to test that genes are passed to the query correctly.
They do not test the API,
as tests of data returned by realworld API queries are best left to integrations tests.
"""
from io import StringIO
from pathlib import Path

import pandas as pd
import pytest
import requests_mock
from pandas.testing import assert_frame_equal
from requests import HTTPError

from gtexquery.data_handling.request import gtex_request, lut_check

from ..custom_tmp_file import GTEX_CONTENTS, GTEX_RESPONSE

lut = pd.DataFrame.from_dict({"name": ["abc", "def"], "id": ["a1", "a2"]})


def test_return_none() -> None:
    """It returns gene when the gene is not found."""
    result = lut_check("ghi", lut)
    assert result == "ghi"


def test_return_str() -> None:
    """It returns the id when the gene is found."""
    result = lut_check("abc", lut)
    assert result == "a1"


def test_no_no_output(tmp_path: Path) -> None:
    """It doesn't output a file when the gene is not found."""
    output = tmp_path / "phony.csv"
    with pytest.raises(SystemExit):
        gtex_request("phony", "phony", str(output))
    assert not output.is_file(), "The file was created."


def test_raises_http_error(tmp_path: Path) -> None:
    """It raises an HTTPError."""
    output = tmp_path / "DLX1_message.csv"
    with pytest.raises(HTTPError), requests_mock.Mocker() as m:
        m.get(
            "https://gtexportal.org/rest/v1/expression/mediantranscriptexpression",
            status_code=400,
        )
        gtex_request("Brain_Hypothalamus", "ENSG0000014435.14", str(output))


def test_writes_file(tmp_path: Path) -> None:
    """It writes the file."""
    output = tmp_path / "DLX1_message.csv"
    with requests_mock.Mocker() as m:
        m.get(
            "https://gtexportal.org/rest/v1/expression/mediantranscriptexpression",
            text=GTEX_RESPONSE,
        )
        gtex_request("Brain_Hypothalamus", "ENSG0000014435.14", str(output))

    response = pd.read_csv(output)
    expected = pd.read_csv(StringIO(GTEX_CONTENTS))
    assert_frame_equal(response, expected)
