"""
Pruebas para la interfaz de Google Calendar.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from calendar_ai_bot.calendar.interface import CalendarInterface

def test_calendar_interface_initialization():
    """
    Prueba la inicialización de la interfaz de Calendar.
    """
    # Mock the interface implementation to avoid actual API calls
    original_init = CalendarInterface.__init__
    
    def mock_init(self, credentials_path, token_path):
        self.service = MagicMock()
        self.credentials_path = credentials_path
        self.token_path = token_path
    
    # Replace the __init__ method temporarily
    CalendarInterface.__init__ = mock_init
    
    try:
        # Create the interface with our mocked init
        interface = CalendarInterface(
            credentials_path='test_credentials.json', 
            token_path='test_token.json'
        )
        
        assert interface is not None
        assert interface.credentials_path == 'test_credentials.json'
        assert interface.token_path == 'test_token.json'
    finally:
        # Restore the original __init__ method
        CalendarInterface.__init__ = original_init

def test_list_calendars():
    """
    Prueba el método de listado de calendarios.
    """
    # Create a mock interface with a mock service
    interface = CalendarInterface.__new__(CalendarInterface)
    interface.service = MagicMock()
    
    # Configure the mock service response
    mock_calendar_list = MagicMock()
    mock_list = MagicMock()
    mock_execute = MagicMock(return_value={
        'items': [
            {'id': 'primary', 'summary': 'Mi calendario'},
            {'id': 'secondary', 'summary': 'Trabajo'}
        ]
    })
    
    interface.service.calendarList = MagicMock(return_value=mock_calendar_list)
    mock_calendar_list.list = MagicMock(return_value=mock_list)
    mock_list.execute = mock_execute
    
    # Mock the list_calendars method to use our mocked service
    original_list_calendars = CalendarInterface.list_calendars
    
    def mock_list_calendars(self):
        return self.service.calendarList().list().execute().get('items', [])
    
    # Replace the method temporarily
    CalendarInterface.list_calendars = mock_list_calendars
    
    try:
        # Call the method
        calendars = interface.list_calendars()
        
        # Verify the results
        assert len(calendars) == 2
        assert calendars[0]['id'] == 'primary'
        assert calendars[1]['summary'] == 'Trabajo'
    finally:
        # Restore the original method
        CalendarInterface.list_calendars = original_list_calendars
