"""
Organizador de eventos de calendario con capacidades de optimización.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

import pytz
from dateutil.parser import parse

logger = logging.getLogger(__name__)

class EventOrganizer:
    """
    Clase para organizar y optimizar eventos de calendario.
    """

    def __init__(self, timezone: str = 'America/Santiago'):
        """
        Inicializa el organizador de eventos.

        Args:
            timezone: Zona horaria para procesamiento de eventos
        """
        self.timezone = pytz.timezone(timezone)

    def _parse_event_time(self, time_str: Optional[str]) -> Optional[datetime]:
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

    def find_optimal_time_slot(self, 
                                events: List[Dict[str, Any]], 
                                duration: timedelta, 
                                days_ahead: int = 7, 
                                min_time: str = '09:00', 
                                max_time: str = '17:00') -> Optional[Dict[str, Any]]:
        """
        Encuentra un espacio de tiempo óptimo para un nuevo evento.

        Args:
            events: Lista de eventos existentes
            duration: Duración del nuevo evento
            days_ahead: Número de días a buscar
            min_time: Hora mínima para programar eventos
            max_time: Hora máxima para programar eventos

        Returns:
            Diccionario con información del espacio de tiempo óptimo o None
        """
        now = datetime.now(self.timezone)
        
        # Convertir min_time y max_time a objetos datetime
        min_dt = now.replace(hour=int(min_time.split(':')[0]), 
                              minute=int(min_time.split(':')[1]), 
                              second=0, 
                              microsecond=0)
        max_dt = now.replace(hour=int(max_time.split(':')[0]), 
                              minute=int(max_time.split(':')[1]), 
                              second=0, 
                              microsecond=0)

        # Ordenar eventos existentes
        sorted_events = sorted(
            [e for e in events if self._parse_event_time(e.get('start', {}).get('dateTime'))],
            key=lambda e: self._parse_event_time(e.get('start', {}).get('dateTime'))
        )

        # Buscar espacios libres
        for day in range(days_ahead):
            current_day = now.date() + timedelta(days=day)
            day_start = self.timezone.localize(datetime.combine(current_day, min_dt.time()))
            day_end = self.timezone.localize(datetime.combine(current_day, max_dt.time()))

            # Verificar si el día está completamente libre
            if not sorted_events or all(
                self._parse_event_time(e.get('start', {}).get('dateTime')).date() != current_day 
                for e in sorted_events
            ):
                return {
                    'start': day_start.isoformat(),
                    'end': (day_start + duration).isoformat(),
                    'date': current_day.isoformat()
                }

            # Buscar espacios entre eventos
            for i in range(len(sorted_events)):
                event_start = self._parse_event_time(sorted_events[i].get('start', {}).get('dateTime'))
                event_end = self._parse_event_time(sorted_events[i].get('end', {}).get('dateTime'))

                # Verificar espacio antes del primer evento
                if i == 0 and event_start and event_start.date() == current_day:
                    potential_start = day_start
                    potential_end = potential_start + duration
                    if potential_end <= event_start:
                        return {
                            'start': potential_start.isoformat(),
                            'end': potential_end.isoformat(),
                            'date': current_day.isoformat()
                        }

                # Verificar espacios entre eventos
                if i < len(sorted_events) - 1:
                    next_event_start = self._parse_event_time(sorted_events[i+1].get('start', {}).get('dateTime'))
                    
                    if (event_end and next_event_start and 
                        event_end.date() == current_day and 
                        next_event_start.date() == current_day):
                        potential_start = event_end
                        potential_end = potential_start + duration
                        
                        if potential_end <= next_event_start:
                            return {
                                'start': potential_start.isoformat(),
                                'end': potential_end.isoformat(),
                                'date': current_day.isoformat()
                            }

                # Verificar espacio después del último evento
                if i == len(sorted_events) - 1 and event_end and event_end.date() == current_day:
                    potential_start = event_end
                    potential_end = potential_start + duration
                    
                    if potential_end <= day_end:
                        return {
                            'start': potential_start.isoformat(),
                            'end': potential_end.isoformat(),
                            'date': current_day.isoformat()
                        }

        return None

    def group_events_by_category(self, events: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Agrupa eventos por categorías.

        Args:
            events: Lista de eventos a agrupar

        Returns:
            Diccionario de eventos agrupados por categoría
        """
        categories = {
            'work': [],
            'personal': [],
            'meetings': [],
            'all_day': [],
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

    def optimize_schedule(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Optimiza la programación de eventos.

        Args:
            events: Lista de eventos a optimizar

        Returns:
            Diccionario con información de optimización
        """
        # Agrupar eventos por categoría
        categorized_events = self.group_events_by_category(events)

        # Analizar distribución de eventos
        optimization_report = {
            'total_events': len(events),
            'categories': {
                category: len(events_in_category) 
                for category, events_in_category in categorized_events.items()
            },
            'suggestions': []
        }

        # Identificar posibles mejoras en la programación
        work_events = categorized_events['work']
        if len(work_events) > 3:
            optimization_report['suggestions'].append(
                "Considera consolidar reuniones de trabajo para mejorar la eficiencia"
            )

        personal_events = categorized_events['personal']
        if len(personal_events) < 1:
            optimization_report['suggestions'].append(
                "Considera reservar tiempo para eventos personales"
            )

        return optimization_report
