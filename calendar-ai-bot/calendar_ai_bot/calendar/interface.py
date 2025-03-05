"""
Interfaz para interactuar con la API de Google Calendar.
"""

import logging
from typing import List, Dict, Any, Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

class CalendarInterface:
    """
    Interfaz para operaciones con Google Calendar API.
    """

    def __init__(self, credentials_path: str, token_path: str):
        """
        Inicializa la interfaz de Calendar.

        Args:
            credentials_path: Ruta al archivo de credenciales OAuth
            token_path: Ruta al archivo de token de acceso
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = self._build_service()

    def _build_service(self):
        """
        Construye el servicio de Google Calendar.

        Returns:
            Servicio de Google Calendar
        """
        try:
            creds = Credentials.from_authorized_user_file(self.token_path, 
                ['https://www.googleapis.com/auth/calendar'])
            return build('calendar', 'v3', credentials=creds)
        except Exception as e:
            logger.error(f"Error al construir servicio de Calendar: {e}")
            raise

    def list_calendars(self) -> List[Dict[str, Any]]:
        """
        Lista todos los calendarios del usuario.

        Returns:
            Lista de calendarios
        """
        try:
            results = self.service.calendarList().list().execute()
            return results.get('items', [])
        except HttpError as error:
            logger.error(f"Error al listar calendarios: {error}")
            return []

    def get_events(self, calendar_id: str = 'primary', 
                   time_min: Optional[str] = None, 
                   time_max: Optional[str] = None, 
                   max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Obtiene eventos de un calendario.

        Args:
            calendar_id: ID del calendario (por defecto: primary)
            time_min: Tiempo mínimo para los eventos
            time_max: Tiempo máximo para los eventos
            max_results: Número máximo de resultados

        Returns:
            Lista de eventos
        """
        try:
            events_result = self.service.events().list(
                calendarId=calendar_id, 
                timeMin=time_min,
                timeMax=time_max,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            return events_result.get('items', [])
        except HttpError as error:
            logger.error(f"Error al obtener eventos: {error}")
            return []

    def create_event(self, calendar_id: str, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Crea un nuevo evento en el calendario.

        Args:
            calendar_id: ID del calendario
            event: Detalles del evento

        Returns:
            Evento creado o None si falla
        """
        try:
            created_event = self.service.events().insert(
                calendarId=calendar_id, 
                body=event
            ).execute()
            return created_event
        except HttpError as error:
            logger.error(f"Error al crear evento: {error}")
            return None

    def update_event(self, calendar_id: str, event_id: str, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Actualiza un evento existente.

        Args:
            calendar_id: ID del calendario
            event_id: ID del evento
            event: Detalles actualizados del evento

        Returns:
            Evento actualizado o None si falla
        """
        try:
            updated_event = self.service.events().update(
                calendarId=calendar_id, 
                eventId=event_id, 
                body=event
            ).execute()
            return updated_event
        except HttpError as error:
            logger.error(f"Error al actualizar evento: {error}")
            return None

    def delete_event(self, calendar_id: str, event_id: str) -> bool:
        """
        Elimina un evento.

        Args:
            calendar_id: ID del calendario
            event_id: ID del evento

        Returns:
            True si se eliminó con éxito, False en caso contrario
        """
        try:
            self.service.events().delete(
                calendarId=calendar_id, 
                eventId=event_id
            ).execute()
            return True
        except HttpError as error:
            logger.error(f"Error al eliminar evento: {error}")
            return False
