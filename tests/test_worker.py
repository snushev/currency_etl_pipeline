import pytest
import pandas as pd
from datetime import datetime
from app.worker import process_data

def test_process_data_success():
    """Test for success data transformation"""
    
    input_data = {
        'date': '2025-10-22',
        'rates': {
            'USD': 1.0,
            'EUR': 0.85,
            'GBP': 0.73
        }
    }

    result = process_data(input_data)

    assert result is not None
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3
    assert list(result.columns) == ['currency', 'rate', 'reference_date',
                                    'created_at', 'created_at_converted']


def test_process_empty_input():
    """Tests for empty input"""

    assert process_data(None) is None
    assert process_data({}) is None


def test_process_data_missing_rates():
    """Tests for missing 'rates' key"""

    input_data = {'date': '2025-10-22'}
    assert process_data(input_data) is None

    
def test_process_data_type_conversion():
    """Tests for correct type conversion"""

    input_data = {
        'date': '2025-10-22',
        'rates': {'USD': 1.5}
    }

    result = process_data(input_data)

    assert result is not None
    assert result['rate'].dtype == float
    assert result['currency'].dtype == object

def test_process_data_with_mock_time( mocker):
        """Тест с mock-нато време"""

        mock_time = datetime(2025, 10, 22, 12, 0, 0)
        mocker.patch('app.helpers.get_current_time', return_value=mock_time)
        mocker.patch('app.helpers.convert_timezone', return_value=mock_time)
        
        input_data = {
            'date': '2025-10-22',
            'rates': {'USD': 1.0}
        }

        result = process_data(input_data)

        assert result is not None
        assert result['created_at'].iloc[0] == mock_time
