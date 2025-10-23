import pytest
import pandas as pd
from app.db_loader import get_connection, create_table, load_to_db


def test_get_connection_success(mocker):
    """Test successful database connection"""
    mock_conn = mocker.Mock()
    mock_connect = mocker.patch('app.db_loader.psycopg2.connect', return_value=mock_conn)
    
    result = get_connection()
    
    assert result is not None
    assert result == mock_conn
    mock_connect.assert_called_once()


def test_get_connection_failure(mocker):
    """Test failed database connection"""
    mocker.patch('app.db_loader.psycopg2.connect', side_effect=Exception("Connection failed"))
    
    result = get_connection()
    
    assert result is None


def test_create_table_success(mocker):
    """Test successful table creation"""
    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mocker.patch('app.db_loader.get_connection', return_value=mock_conn)
    
    create_table()
    
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


def test_create_table_no_connection(mocker):
    """Test table creation when connection fails"""
    mocker.patch('app.db_loader.get_connection', return_value=None)
    
    create_table()


def test_load_to_db_success(mocker):
    """Test successful data load to database"""
    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mocker.patch('app.db_loader.get_connection', return_value=mock_conn)
    mocker.patch('app.db_loader.execute_values')
    
    df = pd.DataFrame({
        'currency': ['USD', 'EUR'],
        'rate': [1.0, 0.85],
        'reference_date': ['2025-10-22', '2025-10-22'],
        'created_at': [pd.Timestamp.now(), pd.Timestamp.now()],
        'created_at_converted': [pd.Timestamp.now(), pd.Timestamp.now()]
    })
    
    load_to_db(df)
    
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()


def test_load_to_db_empty_dataframe():
    """Test loading empty dataframe"""
    df = pd.DataFrame()
    load_to_db(df)


def test_load_to_db_none():
    """Test loading None input"""
    load_to_db(None)


def test_load_to_db_connection_failure(mocker):
    """Test loading when database connection fails"""
    mocker.patch('app.db_loader.get_connection', return_value=None)
    df = pd.DataFrame({'currency': ['USD']})
    
    load_to_db(df)


def test_load_to_db_insert_error(mocker):
    """Test handling of insert errors"""
    mock_cursor = mocker.MagicMock()
    mock_conn = mocker.MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mocker.patch('app.db_loader.get_connection', return_value=mock_conn)
    mock_execute_values = mocker.patch('app.db_loader.execute_values', side_effect=Exception("Insert failed"))
    
    df = pd.DataFrame({
        'currency': ['USD'],
        'rate': [1.0],
        'reference_date': ['2025-10-22'],
        'created_at': [pd.Timestamp.now()],
        'created_at_converted': [pd.Timestamp.now()]
    })
    
    load_to_db(df)
    
    mock_conn.close.assert_called_once()
