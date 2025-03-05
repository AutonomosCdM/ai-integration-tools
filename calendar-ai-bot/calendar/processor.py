"""
Procesador de eventos de calendario con capacidades de análisis.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple

import pytz
from dateutil.parser import parse

logger = logging.getLogger(__name__)

class EventProcessor:
    """
    Clase para procesar y analizar eventos de calendario.
    """

    def __init__(self, timezone: str = 'America/Santiago'):
        """
        Inicializa el procesador de eventos.

        Args:
            timezone: Zona horaria para procesamiento de eventos
        """
        self.timezone = pytz.timezone(timezone)

    def parse_event_time(self, time_str: Optional[str]) -> Optional[datetime]:
        """
        Convierte una cadena de tiempo a datetime con zona horaria.

        Args:
            time_str: Cadena de tiempo en formato ISO o legible

        Returns:
            Datetime con zona horaria o None
        """
        if not time_str:
            return None
        
        try:
            dt = parse(time_str)
            if dt.tzinfo is None:
                dt = self.timezone.localize(dt)
            return dt
        except Exception as e:
            logger.error(f"Error al parsear tiempo: {e}")
            return None

    def calculate_event_duration(self, event: Dict[str, Any]) -> Optional[timedelta]:
        """
        Calcula la duración de un evento.

        Args:
            event: Diccionario de evento de Google Calendar

        Returns:
            Duración del evento como timedelta o None
        """
        try:
            start = self.parse_event_time(event.get('start', {}).get('dateTime'))
            end = self.parse_event_time(event.get('end', {}).get('dateTime'))
            
            if start and end:
                return end - start
            return None
        except Exception as e:
            logger.error(f"Error al calcular duración del evento: {e}")
            return None

    def detect_event_conflicts(self, events: List[Dict[str, Any]]) -> List[Tuple[Dict[str, Any], Dict[str, Any]]]:
        """
        Detecta conflictos de horarios entre eventos.

        Args:
            events: Lista de eventos a comparar

        Returns:
            Lista de tuplas con eventos en conflicto
        """
        conflicts = []
        sorted_events = sorted(events, key=lambda e: self.parse_event_time(e.get('start', {}).get('dateTime')))

        for i in range(len(sorted_events)):
            for j in range(i + 1, len(sorted_events)):
                event1 = sorted_events[i]
                event2 = sorted_events[j]

                start1 = self.parse_event_time(event1.get('start', {}).get('dateTime'))
                end1 = self.parse_event_time(event1.get('end', {}).get('dateTime'))
                start2 = self.parse_event_time(event2.get('start', {}).get('dateTime'))
                end2 = self.parse_event_time(event2.get('end', {}).get('dateTime'))

                if start1 and end1 and start2 and end2:
                    if start2 < end1:
                        conflicts.append((event1, event2))

        return conflicts

    def categorize_events(self, events: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Categoriza eventos por diferentes criterios.

        Args:
            events: Lista de eventos a categorizar

        Returns:
            Diccionario de eventos categorizados
        """
        categories = {
            'all_day': [],
            'meetings': [],
            'personal': [],
            'work': [],
            'recurring': []
        }

        for event in events:
            # Categorización por tipo de evento
            if event.get('start', {}).get('date') and not event.get('start', {}).get('dateTime'):
                categories['all_day'].append(event)
            
            if event.get('recurrence'):
                categories['recurring'].append(event)
            
            # Categorización por título o descripción
            title = event.get('summary', '').lower()
            if any(keyword in title for keyword in ['meeting', 'reunión', 'call', 'llamada']):
                categories['meetings'].append(event)
            
            if any(keyword in title for keyword in ['personal', 'cumpleaños', 'vacaciones']):
                categories['personal'].append(event)
            
            if any(keyword in title for keyword in ['trabajo', 'work', 'project', 'proyecto']):
                categories['work'].append(event)

        return categories

    def extract_event_participants(self, event: Dict[str, Any]) -> List[str]:
        """
        Extrae los participantes de un evento.

        Args:
            event: Evento de Google Calendar

        Returns:
            Lista de correos electrónicos de participantes
        """
        participants = []
        
        # Extraer organizador
        if event.get('organizer', {}).get('email'):
            participants.append(event['organizer']['email'])
        
        # Extraer asistentes
        if event.get('attendees'):
            participants.extend([
                attendee['email'] 
                for attendee in event['attendees'] 
                if 'email' in attendee
            ])
        
        return list(set(participants))  # Eliminar duplicados

    def analyze_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Realiza un análisis completo de un evento.

        Args:
            event: Evento de Google Calendar

        Returns:
            Diccionario con información analizada del evento
        """
        return {
            'id': event.get('id'),
            'title': event.get('summary', 'Sin título'),
            'start_time': self.parse_event_time(event.get('start', {}).get('dateTime')),
            'end_time': self.parse_event_time(event.get('end', {}).get('dateTime')),
            'duration': self.calculate_event_duration(event),
            'participants': self.extract_event_participants(event),
            'is_recurring': bool(event.get('recurrence')),
            'is_all_day': bool(event.get('start', {}).get('date')),
            'description': event.get('description', '')
        }
