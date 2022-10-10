import pytest
import pandas as pd
from mockito import when, forget_invocations, mock
from ..app import CurrencyConversion

@pytest.fixture(scope='module')
def mocked_raw_data():
    raw_data = [{"TIME_PERIOD":"1999-01","OBS_VALUE":1427.6666666667}, \
        {"TIME_PERIOD":"1999-02","OBS_VALUE":379.6666666667}]
    mocked_data = pd.DataFrame(raw_data)
    when(CurrencyConversion, strict=True).get_raw_data(\
        "M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N").thenReturn(mocked_data)
    forget_invocations(CurrencyConversion)
    return CurrencyConversion

@pytest.fixture(scope='module')
def mocked_exchange_rate_data():
    raw_data = [{"TIME_PERIOD":"1999-01","OBS_VALUE":0.7029125}, \
        {"TIME_PERIOD":"1999-02","OBS_VALUE":0.688505}]
    mocked_data = pd.DataFrame(raw_data)
    when(CurrencyConversion, strict=True).get_exchange_rate(\
        "GBP", "EUR").thenReturn(mocked_data)
    forget_invocations(CurrencyConversion)
    return CurrencyConversion

@pytest.fixture(scope='module')
def mocked_raw_data_when_no_data():
    raw_data = []
    mocked_data = pd.DataFrame(raw_data)
    when(CurrencyConversion, strict=True).get_raw_data(\
        "M.N.I8.W1.S1.S1.T.N.FA.F.F7.T.EUR._T.T.N").thenReturn(mocked_data)
    forget_invocations(CurrencyConversion)
    return CurrencyConversion

@pytest.fixture(scope='module')
def mocked_exchange_rate_when_no_data():
    raw_data = []
    mocked_data = pd.DataFrame(raw_data)
    when(CurrencyConversion, strict=True).get_exchange_rate(\
        "GBP", "EUR").thenReturn(mocked_data)
    forget_invocations(CurrencyConversion)
    return CurrencyConversion
