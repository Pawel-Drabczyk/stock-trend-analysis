"""Fixtures for Mocking."""
from unittest.mock import patch

import pytest
import requests_mock

from finance_reports.finance_report_day import SCRAPE_URL


@pytest.fixture
def mock_finance_reports_no_data_response():
    """Mocks a response indicating there's no data for the date."""
    no_data_html = (
        '<table class="cctabdt"><tr><td>Brak wydarzeń do wyświetlenia</td></tr></table>'
    )
    with requests_mock.Mocker() as m:
        m.get(SCRAPE_URL + "2022-01-01", text=no_data_html)
        yield


@pytest.fixture
def mock_finance_reports_data_response():
    """Mocks a response with sample data"""
    data_html = """
    <table class="cctabdt">
        <tr><td><a href="testing">Sample Company</a></td><td><a>SYM1</a></td><td>Report Type 1</td><td>Description 1</td></tr>
        <tr><td><a href="testing">Another Company</a></td><td><a>SYM2</a></td><td>Report Type 2</td><td>Description 2</td></tr>
    </table>
    """
    with requests_mock.Mocker() as m:
        m.get(SCRAPE_URL + "2022-01-02", text=data_html)
        yield


@pytest.fixture
def mock_finance_reports_combined_response():
    """Mocks responses for 2 consecutive dates."""
    no_data_html = (
        '<table class="cctabdt"><tr><td>Brak wydarzeń do wyświetlenia</td></tr></table>'
    )
    data_html = """
    <table class="cctabdt">
        <tr><td><a href="testing">Sample Company</a></td><td><a>SYM1</a></td><td>Report Type 1</td><td>Description 1</td></tr>
        <tr><td><a href="testing">Another Company</a></td><td><a>SYM2</a></td><td>Report Type 2</td><td>Description 2</td></tr>
    </table>
    """
    with requests_mock.Mocker() as m:
        m.get(SCRAPE_URL + "2022-01-01", text=no_data_html)
        m.get(SCRAPE_URL + "2022-01-02", text=data_html)
        yield


@pytest.fixture
def mock_finance_reports_malformed_data_response():
    """Mocks a response with a malformed table"""
    malformed_html = """
    <table class="cctabdt">
        <tr><td><a href="testing">Sample Company</a></td><td>Report Type 1</td><td>Description 1</td></tr>
        <tr><td><a href="testing">Another Company</a></td><td><a>SYM2</a></td><td>Report Type 2</td><td>Description 2</td></tr>
    </table>
    """
    with requests_mock.Mocker() as m:
        m.get(SCRAPE_URL + "2022-01-03", text=malformed_html)
        yield


@pytest.fixture
def mock_finance_reports_content_extraction_response():
    """Mocks a response with a well-formed table."""
    well_formed_html = """
    <table class="cctabdt">
        <tr><td><a>Sample Company</a></td><td><a>SYM1</a></td><td>Report Type 1</td><td>Description 1</td></tr>
        <tr><td><a>Another Company</a></td><td><a>SYM2</a></td><td>Report Type 2</td><td>Description 2</td></tr>
    </table>
    """
    with requests_mock.Mocker() as m:
        m.get(SCRAPE_URL + "2022-01-03", text=well_formed_html)
        yield


@pytest.fixture
def mock_finance_report_day():
    with patch("finance_reports.main.FinanceReportDay") as MockClass:
        yield MockClass()


@pytest.fixture
def mock_gcs_wrapper_from_finance_reports():
    with patch("finance_reports.main.GCSWrapper") as MockClass:
        yield MockClass()
