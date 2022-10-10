import pandas as pd
import pytest
from ..app import CurrencyConversion

def test_exchange_rate_when_source_not_provided():
    with pytest.raises(Exception) as excifo:
        CurrencyConversion.get_exchange_rate("")
    assert str(excifo.value) == 'Source is required'

def test_exchange_rate_when_target_is_not_correct():
    with pytest.raises(Exception) as excifo:
        CurrencyConversion.get_exchange_rate("GBP", "EU")
    assert str(excifo.value) == 'No results found.'

def test_exchange_rate_when_failed():
    with pytest.raises(Exception) as excifo:
        CurrencyConversion.get_exchange_rate("GB")
    assert str(excifo.value) == 'No results found.'

def test_exchange_rate_when_success():
    data = CurrencyConversion.get_exchange_rate("GBP")
    assert isinstance(data, pd.DataFrame)
    collist = data.columns.tolist()
    assert collist == ['TIME_PERIOD','OBS_VALUE']

def test_get_raw_data_when_identifier_not_provided():
    with pytest.raises(Exception) as excifo:
        CurrencyConversion.get_raw_data("")
    assert str(excifo.value) == 'identifier is required'

def test_get_raw_data_when_incorrect_idntifier():
    error_msg = 'Validation error: Mismatch between the number of '+\
    'dimensions used in the series keys (M.N.I8.W1.S1.S1) and the '+\
    'number of dimensions defined in the data structure definition (16).'
    with pytest.raises(Exception) as excifo:
        CurrencyConversion.get_raw_data("M.N.I8.W1.S1.S1")
    assert str(excifo.value) == error_msg

def test_raw_data_when_success():
    data = CurrencyConversion.get_raw_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N")
    assert isinstance(data, pd.DataFrame)
    collist = data.columns.tolist()
    assert collist == ['TIME_PERIOD','OBS_VALUE']

def test_get_data_when_success_when_no_raw_data(mocked_raw_data_when_no_data, \
    mocked_exchange_rate_data):
    with pytest.raises(Exception) as excifo:
        CurrencyConversion.get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", "GBP")
    assert str(excifo.value) == "No Raw Data Available"

def test_get_data_when_success(mocked_raw_data, mocked_exchange_rate_data):
    data = CurrencyConversion.get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", "GBP")
    assert isinstance(data, pd.DataFrame)
    collist = data.columns.tolist()
    assert collist == ['TIME_PERIOD', 'OBS_VALUE']

def test_get_data_when_no_target_currency(mocked_raw_data, mocked_exchange_rate_data):
    data = CurrencyConversion.get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N")
    assert isinstance(data, pd.DataFrame)
    collist = data.columns.tolist()
    assert collist == ['TIME_PERIOD', 'OBS_VALUE']

def test_get_data_when_success_when_no_exchange_rate_data(mocked_raw_data, \
    mocked_exchange_rate_when_no_data):
    with pytest.raises(Exception) as excifo:
        CurrencyConversion.get_data("M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N", "GBP")
    assert str(excifo.value) == "No Exchange Data Available"