"""
Módulo de integración con Calendar.
"""

from .interface import CalendarInterface
from .processor import EventProcessor
from .organizer import EventOrganizer
from .filters import CalendarFilter

__all__ = [
    'CalendarInterface',
    'EventProcessor',
    'EventOrganizer',
    'CalendarFilter'
]
