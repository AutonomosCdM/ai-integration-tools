"""
Módulo de filtros para eventos de calendario.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Callable, Optional, Union

import pytz
from dateutil.parser import parse

logger = logging.getLogger(__name__)

class CalendarFilter:
    """
    Clase para filtrar y manipular eventos de calendario.
    """

    def __init__(self, timezone: str = 'America/Santiago'):
        """
        Inicializa el filtro de calendario.

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

    def filter_by_date_range(self, 
                              events: List[Dict[str, Any]], 
                              start_date: Optional[Union[str, datetime]] = None, 
                              end_date: Optional[Union[str, datetime]] = None) -> List[Dict[str, Any]]:
        """
        Filtra eventos dentro de un rango de fechas.

        Args:
            events: Lista de eventos a filtrar
            start_date: Fecha de inicio del rango (inclusive)
            end_date: Fecha de fin del rango (inclusive)

        Returns:
            Lista de eventos dentro del rango de fechas
        """
        # Convertir fechas a datetime si son cadenas
        if isinstance(start_date, str):
            start_date = self._parse_event_time(start_date)
        if isinstance(end_date, str):
            end_date = self._parse_event_time(end_date)

        # Si no se proporcionan fechas, usar rango completo
        if not start_date:
            start_date = datetime.min.replace(tzinfo=self.timezone)
        if not end_date:
            end_date = datetime.max.replace(tzinfo=self.timezone)

        filtered_events = []
        for event in events:
            event_start = self._parse_event_time(event.get('start', {}).get('dateTime'))
            
            if event_start and start_date <= event_start <= end_date:
                filtered_events.append(event)

        return filtered_events

    def filter_by_title(self, 
                        events: List[Dict[str, Any]], 
                        keywords: Union[str, List[str]], 
                        case_sensitive: bool = False) -> List[Dict[str, Any]]:
        """
        Filtra eventos por palabras clave en el título.

        Args:
            events: Lista de eventos a filtrar
            keywords: Palabra(s) clave a buscar
            case_sensitive: Si la búsqueda debe ser sensible a mayúsculas/minúsculas

        Returns:
            Lista de eventos que coinciden con las palabras clave
        """
        # Convertir keywords a lista si es una cadena
        if isinstance(keywords, str):
            keywords = [keywords]

        # Convertir a minúsculas si no es sensible a mayúsculas
        if not case_sensitive:
            keywords = [kw.lower() for kw in keywords]

        filtered_events = []
        for event in events:
            title = event.get('summary', '')
            
            # Ajustar título según sensibilidad de mayúsculas
            check_title = title if case_sensitive else title.lower()
            
            # Verificar si alguna palabra clave está en el título
            if any(kw in check_title for kw in keywords):
                filtered_events.append(event)

        return filtered_events

    def filter_by_participants(self, 
                                events: List[Dict[str, Any]], 
                                participants: Union[str, List[str]]) -> List[Dict[str, Any]]:
        """
        Filtra eventos por participantes.

        Args:
            events: Lista de eventos a filtrar
            participants: Correo(s) de participante(s)

        Returns:
            Lista de eventos con los participantes especificados
        """
        # Convertir participants a lista si es una cadena
        if isinstance(participants, str):
            participants = [participants]

        filtered_events = []
        for event in events:
            event_participants = set()
            
            # Extraer correos de organizador
            if event.get('organizer', {}).get('email'):
                event_participants.add(event['organizer']['email'])
            
            # Extraer correos de asistentes
            if event.get('attendees'):
                event_participants.update(
                    attendee['email'] 
                    for attendee in event['attendees'] 
                    if 'email' in attendee
                )

            # Verificar si algún participante coincide
            if any(p in event_participants for p in participants):
                filtered_events.append(event)

        return filtered_events

    def filter_by_duration(self, 
                            events: List[Dict[str, Any]], 
                            min_duration: Optional[timedelta] = None, 
                            max_duration: Optional[timedelta] = None) -> List[Dict[str, Any]]:
        """
        Filtra eventos por duración.

        Args:
            events: Lista de eventos a filtrar
            min_duration: Duración mínima del evento
            max_duration: Duración máxima del evento

        Returns:
            Lista de eventos dentro del rango de duración
        """
        filtered_events = []
        for event in events:
            start = self._parse_event_time(event.get('start', {}).get('dateTime'))
            end = self._parse_event_time(event.get('end', {}).get('dateTime'))
            
            if start and end:
                duration = end - start
                
                # Verificar condiciones de duración
                if ((min_duration is None or duration >= min_duration) and
                    (max_duration is None or duration <= max_duration)):
                    filtered_events.append(event)

        return filtered_events

    def filter_by_custom_rule(self, 
                               events: List[Dict[str, Any]], 
                               rule: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
        """
        Filtra eventos usando una regla personalizada.

        Args:
            events: Lista de eventos a filtrar
            rule: Función que toma un evento y devuelve un booleano

        Returns:
            Lista de eventos que cumplen la regla
        """
        return [event for event in events if rule(event)]

    def combine_filters(self, 
                        events: List[Dict[str, Any]], 
                        *filter_funcs: Callable[[List[Dict[str, Any]]], List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Combina múltiples filtros secuencialmente.

        Args:
            events: Lista de eventos inicial
            filter_funcs: Funciones de filtro a aplicar secuencialmente

        Returns:
            Lista de eventos después de aplicar todos los filtros
        """
        result = events
        for filter_func in filter_funcs:
            result = filter_func(result)
        return result
