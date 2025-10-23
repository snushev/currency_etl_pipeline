import pytest
import requests
from app.requester import fetch_data

def test_fetch_data_success(mocker):
    """Test for successfully fetch data"""

    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        'date': '2025-10-22',
        'rates': {'USD': 1.0, 'EUR': 0.85}
    }
    mock_response.status_code = 200
    mock_get = mocker.patch("app.requester.requests.get", return_value=mock_response)

    result = fetch_data()

    assert result is not None
    assert result['date'] == '2025-10-22'
    assert 'rates' in result
    mock_get.assert_called_once()

def test_fetch_data_timeout(mocker):
    """Tests for timeout error"""

    mocker.patch("app.requester.requests.get", side_effect=requests.exceptions.Timeout())

    result = fetch_data()

    assert result is None

def test_fetch_data_http_error(mocker):
    """Tests for HTTP error(404, 500, etc)"""

    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
    mocker.patch("app.requester.requests.get", return_value=mock_response)

    result = fetch_data()

    assert result is None

def test_fetch_data_no_api_url(mocker):
    mocker.patch('app.config.API_URL', '')

    with pytest.raises(ValueError, match="API_URL is not set"):
            fetch_data()

def test_fetch_data_invalid_json(mocker):
    """Tests for invalid JSON response"""

    mock_response = mocker.Mock()
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mocker.patch("app.requester.requests.get", return_value=mock_response)

    with pytest.raises(ValueError, match="Invalid JSON"):
            fetch_data()
