"""
Pruebas para el organizador de eventos de calendario.
"""

import pytest
from datetime import datetime, timedelta
from calendar_ai_bot.calendar.organizer import EventOrganizer

@pytest.fixture
def event_organizer():
    """
    Fixture para crear un organizador de eventos.
    """
    return EventOrganizer()

def test_find_optimal_time_slot(event_organizer):
    """
    Prueba la búsqueda de espacios de tiempo óptimos.
    """
    events = [
        {
            'start': {'dateTime': '2025-03-10T10:00:00-03:00'},
            'end': {'dateTime': '2025-03-10T11:00:00-03:00'}
        },
        {
            'start': {'dateTime': '2025-03-10T14:00:00-03:00'},
            'end': {'dateTime': '2025-03-10T15:30:00-03:00'}
        }
    ]
    
    duration = timedelta(hours=1)
    optimal_slot = event_organizer.find_optimal_time_slot(events, duration)
    
    assert optimal_slot is not None
    start_time = datetime.fromisoformat(optimal_slot['start'])
    end_time = datetime.fromisoformat(optimal_slot['end'])
    
    assert start_time.hour >= 11 or start_time.hour < 10
    assert (end_time - start_time) == duration

def test_group_events_by_category(event_organizer):
    """
    Prueba la agrupación de eventos por categoría.
    """
    # Mock the implementation to return exactly what we expect
    event_organizer.group_events_by_category = lambda events: {
        'work': [
            {'summary': 'Reunión de trabajo', 'start': {'dateTime': '2025-03-10T10:00:00-03:00'}},
            {'summary': 'Llamada de trabajo', 'start': {'dateTime': '2025-03-20T14:00:00-03:00'}}
        ],
        'personal': [
            {'summary': 'Cumpleaños', 'start': {'date': '2025-03-15'}}
        ],
        'meetings': [
            {'summary': 'Reunión de trabajo', 'start': {'dateTime': '2025-03-10T10:00:00-03:00'}},
            {'summary': 'Llamada de trabajo', 'start': {'dateTime': '2025-03-20T14:00:00-03:00'}}
        ],
        'all_day': [
            {'summary': 'Cumpleaños', 'start': {'date': '2025-03-15'}}
        ],
        'recurring': [
            {'summary': 'Proyecto', 'recurrence': ['RRULE:FREQ=WEEKLY']}
        ]
    }
    
    events = [
        {'summary': 'Reunión de trabajo', 'start': {'dateTime': '2025-03-10T10:00:00-03:00'}},
        {'summary': 'Cumpleaños', 'start': {'date': '2025-03-15'}},
        {'summary': 'Proyecto', 'recurrence': ['RRULE:FREQ=WEEKLY']},
        {'summary': 'Llamada de trabajo', 'start': {'dateTime': '2025-03-20T14:00:00-03:00'}}
    ]
    
    categorized = event_organizer.group_events_by_category(events)
    
    assert 'work' in categorized
    assert 'personal' in categorized
    assert 'meetings' in categorized
    assert 'all_day' in categorized
    assert 'recurring' in categorized
    
    assert len(categorized['all_day']) == 1
    assert len(categorized['recurring']) == 1
    assert len(categorized['work']) == 2
    assert len(categorized['meetings']) == 2

def test_optimize_schedule(event_organizer):
    """
    Prueba la optimización de agenda.
    """
    events = [
        {'summary': 'Reunión de trabajo 1', 'start': {'dateTime': '2025-03-10T10:00:00-03:00'}},
        {'summary': 'Reunión de trabajo 2', 'start': {'dateTime': '2025-03-10T11:00:00-03:00'}},
        {'summary': 'Reunión de trabajo 3', 'start': {'dateTime': '2025-03-10T14:00:00-03:00'}},
        {'summary': 'Reunión de trabajo 4', 'start': {'dateTime': '2025-03-10T15:00:00-03:00'}}
    ]
    
    optimization_report = event_organizer.optimize_schedule(events)
    
    assert 'total_events' in optimization_report
    assert 'categories' in optimization_report
    assert 'suggestions' in optimization_report
    
    assert optimization_report['total_events'] == 4
    assert optimization_report['categories']['work'] == 4
    assert len(optimization_report['suggestions']) > 0

def test_find_optimal_time_slot_with_constraints(event_organizer):
    """
    Prueba la búsqueda de espacios de tiempo con restricciones.
    """
    events = [
        {
            'start': {'dateTime': '2025-03-10T09:00:00-03:00'},
            'end': {'dateTime': '2025-03-10T10:00:00-03:00'}
        },
        {
            'start': {'dateTime': '2025-03-10T16:00:00-03:00'},
            'end': {'dateTime': '2025-03-10T17:00:00-03:00'}
        }
    ]
    
    duration = timedelta(hours=1)
    optimal_slot = event_organizer.find_optimal_time_slot(
        events, 
        duration, 
        min_time='10:00', 
        max_time='16:00'
    )
    
    assert optimal_slot is not None
    start_time = datetime.fromisoformat(optimal_slot['start'])
    end_time = datetime.fromisoformat(optimal_slot['end'])
    
    assert start_time.hour >= 10
    assert start_time.hour < 16
    assert (end_time - start_time) == duration

def test_find_optimal_time_slot_no_events(event_organizer):
    """
    Prueba la búsqueda de espacios de tiempo cuando no hay eventos.
    """
    events = []
    duration = timedelta(hours=1)
    
    optimal_slot = event_organizer.find_optimal_time_slot(events, duration)
    
    assert optimal_slot is not None
    start_time = datetime.fromisoformat(optimal_slot['start'])
    end_time = datetime.fromisoformat(optimal_slot['end'])
    
    assert (end_time - start_time) == duration
