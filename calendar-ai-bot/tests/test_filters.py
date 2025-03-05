"""
Pruebas para los filtros de eventos de calendario.
"""

import pytest
from datetime import datetime, timedelta
from calendar_ai_bot.calendar.filters import CalendarFilter

@pytest.fixture
def calendar_filter():
    """
    Fixture para crear un filtro de calendario.
    """
    return CalendarFilter()

def test_filter_by_date_range(calendar_filter):
    """
    Prueba el filtrado de eventos por rango de fechas.
    """
    events = [
        {
            'start': {'dateTime': '2025-03-01T10:00:00-03:00'},
            'summary': 'Evento 1'
        },
        {
            'start': {'dateTime': '2025-03-15T14:00:00-03:00'},
            'summary': 'Evento 2'
        },
        {
            'start': {'dateTime': '2025-04-01T09:00:00-03:00'},
            'summary': 'Evento 3'
        }
    ]
    
    filtered_events = calendar_filter.filter_by_date_range(
        events, 
        start_date='2025-03-10', 
        end_date='2025-03-31'
    )
    
    assert len(filtered_events) == 1
    assert filtered_events[0]['summary'] == 'Evento 2'

def test_filter_by_title(calendar_filter):
    """
    Prueba el filtrado de eventos por título.
    """
    events = [
        {'summary': 'Reunión de trabajo'},
        {'summary': 'Llamada de proyecto'},
        {'summary': 'Cumpleaños familiar'}
    ]
    
    filtered_events = calendar_filter.filter_by_title(events, ['trabajo', 'proyecto'])
    
    assert len(filtered_events) == 2
    assert any(event['summary'] == 'Reunión de trabajo' for event in filtered_events)
    assert any(event['summary'] == 'Llamada de proyecto' for event in filtered_events)

def test_filter_by_title_case_sensitive(calendar_filter):
    """
    Prueba el filtrado de eventos por título con sensibilidad a mayúsculas.
    """
    events = [
        {'summary': 'Reunión de Trabajo'},
        {'summary': 'llamada de proyecto'},
        {'summary': 'Cumpleaños Familiar'}
    ]
    
    filtered_events_case_insensitive = calendar_filter.filter_by_title(events, ['trabajo'], case_sensitive=False)
    filtered_events_case_sensitive = calendar_filter.filter_by_title(events, ['trabajo'], case_sensitive=True)
    
    assert len(filtered_events_case_insensitive) == 1
    assert len(filtered_events_case_sensitive) == 0

def test_filter_by_participants(calendar_filter):
    """
    Prueba el filtrado de eventos por participantes.
    """
    events = [
        {
            'summary': 'Reunión 1',
            'attendees': [{'email': 'usuario1@example.com'}],
            'organizer': {'email': 'organizador@example.com'}
        },
        {
            'summary': 'Reunión 2',
            'attendees': [{'email': 'usuario2@example.com'}],
            'organizer': {'email': 'otro@example.com'}
        }
    ]
    
    filtered_events = calendar_filter.filter_by_participants(events, ['usuario1@example.com'])
    
    assert len(filtered_events) == 1
    assert filtered_events[0]['summary'] == 'Reunión 1'

def test_filter_by_duration(calendar_filter):
    """
    Prueba el filtrado de eventos por duración.
    """
    events = [
        {
            'start': {'dateTime': '2025-03-10T10:00:00-03:00'},
            'end': {'dateTime': '2025-03-10T11:00:00-03:00'}
        },
        {
            'start': {'dateTime': '2025-03-10T14:00:00-03:00'},
            'end': {'dateTime': '2025-03-10T15:30:00-03:00'}
        },
        {
            'start': {'dateTime': '2025-03-10T16:00:00-03:00'},
            'end': {'dateTime': '2025-03-10T16:15:00-03:00'}
        }
    ]
    
    filtered_events = calendar_filter.filter_by_duration(
        events, 
        min_duration=timedelta(minutes=30), 
        max_duration=timedelta(hours=1, minutes=30)
    )
    
    assert len(filtered_events) == 2
    assert all(
        timedelta(minutes=30) <= 
        (datetime.fromisoformat(event['end']['dateTime']) - datetime.fromisoformat(event['start']['dateTime'])) <= 
        timedelta(hours=1, minutes=30) 
        for event in filtered_events
    )

def test_filter_by_custom_rule(calendar_filter):
    """
    Prueba el filtrado de eventos con una regla personalizada.
    """
    events = [
        {'summary': 'Reunión de trabajo', 'start': {'dateTime': '2025-03-10T10:00:00-03:00'}},
        {'summary': 'Evento personal', 'start': {'dateTime': '2025-03-15T14:00:00-03:00'}},
        {'summary': 'Conferencia', 'start': {'dateTime': '2025-03-20T09:00:00-03:00'}}
    ]
    
    def custom_rule(event):
        return 'trabajo' in event['summary'] or 'Conferencia' in event['summary']
    
    filtered_events = calendar_filter.filter_by_custom_rule(events, custom_rule)
    
    assert len(filtered_events) == 2
    assert any(event['summary'] == 'Reunión de trabajo' for event in filtered_events)
    assert any(event['summary'] == 'Conferencia' for event in filtered_events)

def test_combine_filters(calendar_filter):
    """
    Prueba la combinación de múltiples filtros.
    """
    events = [
        {
            'summary': 'Reunión de trabajo',
            'start': {'dateTime': '2025-03-10T10:00:00-03:00'},
            'end': {'dateTime': '2025-03-10T11:00:00-03:00'},
            'attendees': [{'email': 'usuario1@example.com'}]
        },
        {
            'summary': 'Llamada de proyecto',
            'start': {'dateTime': '2025-03-15T14:00:00-03:00'},
            'end': {'dateTime': '2025-03-15T15:30:00-03:00'},
            'attendees': [{'email': 'usuario2@example.com'}]
        },
        {
            'summary': 'Evento personal',
            'start': {'dateTime': '2025-03-20T09:00:00-03:00'},
            'end': {'dateTime': '2025-03-20T10:00:00-03:00'},
            'attendees': [{'email': 'usuario1@example.com'}]
        }
    ]
    
    def title_filter(events):
        return calendar_filter.filter_by_title(events, ['trabajo', 'proyecto'])
    
    def participant_filter(events):
        return calendar_filter.filter_by_participants(events, ['usuario1@example.com'])
    
    def duration_filter(events):
        return calendar_filter.filter_by_duration(events, min_duration=timedelta(hours=1))
    
    combined_filtered_events = calendar_filter.combine_filters(
        events, 
        title_filter, 
        participant_filter, 
        duration_filter
    )
    
    assert len(combined_filtered_events) == 1
    assert combined_filtered_events[0]['summary'] == 'Reunión de trabajo'
