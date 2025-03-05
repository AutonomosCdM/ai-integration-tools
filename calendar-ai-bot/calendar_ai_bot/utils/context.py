"""
Módulo de gestión de contexto para Calendar AI Bot.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

import pytz

logger = logging.getLogger(__name__)

class ContextManager:
    """
    Gestiona el contexto de eventos y operaciones del calendario.
    """

    def __init__(self, timezone: str = 'America/Santiago'):
        """
        Inicializa el gestor de contexto.

        Args:
            timezone: Zona horaria para procesamiento de eventos
        """
        self.timezone = pytz.timezone(timezone)
        self.context_history: List[Dict[str, Any]] = []
        self.current_context: Dict[str, Any] = {}

    def update_context(self, events: List[Dict[str, Any]], operation: str = 'sync') -> None:
        """
        Actualiza el contexto con una lista de eventos.

        Args:
            events: Lista de eventos de Google Calendar
            operation: Tipo de operación realizada (sync, create, update, delete)
        """
        try:
            context_entry = {
                'timestamp': datetime.now(self.timezone).isoformat(),
                'operation': operation,
                'events_count': len(events),
                'events': events
            }

            # Agregar a historial de contexto
            self.context_history.append(context_entry)

            # Mantener solo los últimos 100 registros de contexto
            if len(self.context_history) > 100:
                self.context_history = self.context_history[-100:]

            # Actualizar contexto actual
            self.current_context = context_entry
            
            logger.info(f"Contexto actualizado: {operation} - {len(events)} eventos")
        except Exception as e:
            logger.error(f"Error al actualizar contexto: {e}")

    def get_recent_context(self, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Obtiene el contexto de eventos recientes.

        Args:
            hours: Número de horas hacia atrás para recuperar contexto

        Returns:
            Lista de entradas de contexto dentro del rango de tiempo
        """
        try:
            cutoff_time = datetime.now(self.timezone) - timedelta(hours=hours)
            
            recent_context = [
                entry for entry in self.context_history
                if datetime.fromisoformat(entry['timestamp']) >= cutoff_time
            ]
            
            return recent_context
        except Exception as e:
            logger.error(f"Error al obtener contexto reciente: {e}")
            return []

    def analyze_context_patterns(self) -> Dict[str, Any]:
        """
        Analiza patrones en el contexto histórico.

        Returns:
            Diccionario con insights sobre patrones de eventos
        """
        try:
            # Análisis de operaciones
            operations = [entry['operation'] for entry in self.context_history]
            operation_counts = {
                op: operations.count(op) for op in set(operations)
            }

            # Análisis de eventos
            total_events = sum(entry['events_count'] for entry in self.context_history)
            avg_events_per_operation = total_events / len(self.context_history) if self.context_history else 0

            # Análisis de frecuencia temporal
            timestamps = [datetime.fromisoformat(entry['timestamp']) for entry in self.context_history]
            time_deltas = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
            avg_time_between_operations = sum(time_deltas, timedelta()) / len(time_deltas) if time_deltas else timedelta()

            return {
                'operation_counts': operation_counts,
                'total_events': total_events,
                'avg_events_per_operation': avg_events_per_operation,
                'avg_time_between_operations': avg_time_between_operations.total_seconds(),
                'context_entries': len(self.context_history)
            }
        except Exception as e:
            logger.error(f"Error al analizar patrones de contexto: {e}")
            return {}

    def find_context_by_criteria(self, 
                                  operation: Optional[str] = None, 
                                  min_events: Optional[int] = None, 
                                  max_events: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Busca entradas de contexto según criterios específicos.

        Args:
            operation: Filtrar por tipo de operación
            min_events: Número mínimo de eventos
            max_events: Número máximo de eventos

        Returns:
            Lista de entradas de contexto que coinciden con los criterios
        """
        try:
            filtered_context = self.context_history

            # Filtrar por operación
            if operation:
                filtered_context = [
                    entry for entry in filtered_context 
                    if entry['operation'] == operation
                ]

            # Filtrar por número de eventos
            if min_events is not None:
                filtered_context = [
                    entry for entry in filtered_context 
                    if entry['events_count'] >= min_events
                ]

            if max_events is not None:
                filtered_context = [
                    entry for entry in filtered_context 
                    if entry['events_count'] <= max_events
                ]

            return filtered_context
        except Exception as e:
            logger.error(f"Error al buscar contexto por criterios: {e}")
            return []

    def clear_context(self) -> None:
        """
        Limpia todo el historial de contexto.
        """
        try:
            self.context_history.clear()
            self.current_context = {}
            logger.info("Historial de contexto limpiado")
        except Exception as e:
            logger.error(f"Error al limpiar contexto: {e}")
