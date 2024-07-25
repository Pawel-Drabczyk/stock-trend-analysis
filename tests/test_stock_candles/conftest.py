"""Fixtures for Mocking."""
from unittest.mock import patch

import pytest
import requests_mock

from stock_candles.constants import SCRAPE_URL


@pytest.fixture
def mock_stock_candles_data_with_header_response():
    """Mocks a response with sample data"""
    data_html = """
    <table class="table footable" data-sorting="true" >
        <thead>
        <tr>
            <th class="left">Nazwa</th>
            <th class="left">Kod ISIN</th>
            <th class="text-right">Waluta</th>
            <th class="text-right" data-type="numeric">Kurs otwarcia</th>
            <th class="text-right" data-type="numeric">Kurs maksymalny</th>
            <th class="text-right" data-type="numeric">Kurs minimalny</th>
            <th class="text-right" data-type="numeric">Kurs zamknięcia</th>
            <th class="text-right" data-type="numeric">Zmiana kursu %</th>
            <th class="text-right" data-type="numeric">Wolumen obrotu (w szt.)</th>
            <th class="text-right" data-type="numeric">Liczba transakcji</th>
            <th class="text-right" data-type="numeric">Wartość obrotu (w tys.)</th>
        </tr>
        </thead>
        <tr>
            <td class="left">Sample Company</td>
            <td class="left">ISIN1</td>
            <td class="text-right">PLN</td>
            <td class="text-right">1,1100</td>
            <td class="text-right">2,2200</td>
            <td class="text-right">2,8000</td>
            <td class="text-right">1,0000</td>
            <td class="text-right">-1,04</td>
            <td class="text-right">4 443</td>
            <td class="text-right">12</td>
            <td class="text-right">12,56</td>
        </tr>
        <tr>
            <td class="left">Another Company</td>
            <td class="left">ISIN2</td>
            <td class="text-right">EUR</td>
            <td class="text-right">1,0800</td>
            <td class="text-right">1,0800</td>
            <td class="text-right">1,0800</td>
            <td class="text-right">1,0800</td>
            <td class="text-right">4,85</td>
            <td class="text-right">100</td>
            <td class="text-right">2</td>
            <td class="text-right">0,11</td>
        </tr>
    </table>
    """
    with requests_mock.Mocker() as m:
        m.get(SCRAPE_URL + "01-01-2022", text=data_html)
        yield


@pytest.fixture
def mock_stock_candles_data_without_header_response():
    """Mocks a response with sample data"""
    data_html = """
    <table class="table footable" data-sorting="true" >
        <tr>
            <td class="left">Sample Company</td>
            <td class="left">ISIN1</td>
            <td class="text-right">PLN</td>
            <td class="text-right">1,1100</td>
            <td class="text-right">2,2200</td>
            <td class="text-right">2,8000</td>
            <td class="text-right">1,0000</td>
            <td class="text-right">-1,04</td>
            <td class="text-right">4 443</td>
            <td class="text-right">12</td>
            <td class="text-right">12,56</td>
        </tr>
        <tr>
            <td class="left">Another Company</td>
            <td class="left">ISIN2</td>
            <td class="text-right">EUR</td>
            <td class="text-right">1,0800</td>
            <td class="text-right">1,0800</td>
            <td class="text-right">1,0800</td>
            <td class="text-right">1,0800</td>
            <td class="text-right">4,85</td>
            <td class="text-right">100</td>
            <td class="text-right">2</td>
            <td class="text-right">0,11</td>
        </tr>
    </table>
    """
    with requests_mock.Mocker() as m:
        m.get(SCRAPE_URL + "01-01-2022", text=data_html)
        yield


@pytest.fixture
def mock_stock_candles_no_data_response():
    """Mocks a response indicating there's no data for the date"""
    no_data_html = "Brak danych dla wybranych kryteriów."
    with requests_mock.Mocker() as m:
        m.get(SCRAPE_URL + "02-01-2022", text=no_data_html)
        yield


@pytest.fixture
def mock_stock_candles_malformed_data_additional_column_response():
    """Mocks a data with extra column"""
    data_html = """
    <table class="table footable" data-sorting="true" >
        <tr>
            <td class="left">Sample Company</td>
            <td class="left">ISIN1</td>
            <td class="text-right">PLN</td>
            <td class="text-right">1,1100</td>
            <td class="text-right">2,2200</td>
            <td class="text-right">2,8000</td>
            <td class="text-right">1,0000</td>
            <td class="text-right">-1,04</td>
            <td class="text-right">4 443</td>
            <td class="text-right">12</td>
            <td class="text-right">12,56</td>
            <td class="text-right">EXTRA COLUMN</td>
        </tr>
        <tr>
            <td class="left">Another Company</td>
            <td class="left">ISIN2</td>
            <td class="text-right">EUR</td>
            <td class="text-right">1,0800</td>
            <td class="text-right">1,0800</td>
            <td class="text-right">1,0800</td>
            <td class="text-right">1,0800</td>
            <td class="text-right">4,85</td>
            <td class="text-right">100</td>
            <td class="text-right">2</td>
            <td class="text-right">0,11</td>
        </tr>
    </table>
    """
    with requests_mock.Mocker() as m:
        m.get(SCRAPE_URL + "03-01-2022", text=data_html)
        yield


@pytest.fixture
def mock_stock_candles_malformed_data_missing_column_response():
    """Mocks a data with missing column"""
    data_html = """
    <table class="table footable" data-sorting="true" >
        <tr>
            <td class="left">Sample Company</td>
            <td class="left">ISIN1</td>
            <td class="text-right">PLN</td>
            <td class="text-right">1,1100</td>
            <td class="text-right">2,2200</td>
            <td class="text-right">2,8000</td>
            <td class="text-right">1,0000</td>
            <td class="text-right">-1,04</td>
            <td class="text-right">4 443</td>
        </tr>
        <tr>
            <td class="left">Another Company</td>
            <td class="left">ISIN2</td>
            <td class="text-right">EUR</td>
            <td class="text-right">1,0800</td>
            <td class="text-right">1,0800</td>
            <td class="text-right">1,0800</td>
            <td class="text-right">1,0800</td>
            <td class="text-right">4,85</td>
            <td class="text-right">100</td>
            <td class="text-right">2</td>
            <td class="text-right">0,11</td>
        </tr>
    </table>
    """
    with requests_mock.Mocker() as m:
        m.get(SCRAPE_URL + "04-01-2022", text=data_html)
        yield


@pytest.fixture
def mock_stock_candles_malformed_data_missing_td_closing_tag_response():
    """Mocks a malformed data with missing td closing tag."""
    data_html = """
    <table class="table footable" data-sorting="true">
    <tr>
        <td class="left">Another Company</td>
        <td class="left">ISIN2</td>
        <td class="text-right">EUR</td>
        <td class="text-right">1,0800</td>
        <td class="text-right">1,0800</td>
        <tr> <!-- Missing closing </td> and opening <tr> tags -->
        <td class="text-right">1,0800</td>
        <td class="text-right">1,0800</td>
        <td class="text-right">4,85</td>
        <td class="text-right">100</td>
        <td class="text-right">2</td>
        <td class="text-right">0,11</td>
    </tr>
</table>
    """
    with requests_mock.Mocker() as m:
        m.get(SCRAPE_URL + "05-01-2022", text=data_html)
        yield


@pytest.fixture
def mock_stock_candles_malformed_data_missing_table_response():
    """Mocks a malformed data with missing table."""
    data_html = """
        <td class="left">Sample Company</td>
        <td class="left">ISIN1</td>
        <td class="text-right">PLN</td>
        <td class="text-right">1,1100</td>
    """
    with requests_mock.Mocker() as m:
        m.get(SCRAPE_URL + "06-01-2022", text=data_html)
        yield


@pytest.fixture
def mock_stock_candles_combined_response():
    """Mocks responses for 2 consecutive dates."""
    no_data_html = "Brak danych dla wybranych kryteriów."
    data_html = """
    <table class="table footable" data-sorting="true" >
        <tr>
            <td class="left">Sample Company</td>
            <td class="left">ISIN1</td>
            <td class="text-right">PLN</td>
            <td class="text-right">1,1100</td>
            <td class="text-right">2,2200</td>
            <td class="text-right">2,8000</td>
            <td class="text-right">1,0000</td>
            <td class="text-right">-1,04</td>
            <td class="text-right">4 443</td>
            <td class="text-right">12</td>
            <td class="text-right">12,56</td>
        </tr>
        <tr>
            <td class="left">Another Company</td>
            <td class="left">ISIN2</td>
            <td class="text-right">EUR</td>
            <td class="text-right">1,0800</td>
            <td class="text-right">1,0800</td>
            <td class="text-right">1,0800</td>
            <td class="text-right">1,0800</td>
            <td class="text-right">4,85</td>
            <td class="text-right">100</td>
            <td class="text-right">2</td>
            <td class="text-right">0,11</td>
        </tr>
    </table>
    """
    with requests_mock.Mocker() as m:
        m.get(SCRAPE_URL + "11-09-2022", text=no_data_html)
        m.get(SCRAPE_URL + "12-09-2022", text=data_html)
        yield


@pytest.fixture
def mock_stock_candles():
    with patch("stock_candles.main.StockCandles") as MockClass:
        yield MockClass()


@pytest.fixture
def mock_gcs_wrapper_from_stock_candles():
    with patch("stock_candles.main.GCSWrapper") as MockClass:
        yield MockClass()
