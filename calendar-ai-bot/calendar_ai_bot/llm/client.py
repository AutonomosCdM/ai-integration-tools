"""
Cliente de Modelo de Lenguaje para Calendar AI Bot.
"""

import logging
import json
from typing import Dict, Any, Optional, List

import groq
import openai

logger = logging.getLogger(__name__)

class LLMClient:
    """
    Cliente para interactuar con modelos de lenguaje.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa el cliente LLM.

        Args:
            config: Configuración del cliente LLM
        """
        self.config = config
        self.provider = config.get('provider', 'groq')
        self.model = config.get('model', 'llama3-70b-8192')
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 1024)

        # Configurar cliente según el proveedor
        if self.provider == 'groq':
            self.client = groq.Groq(api_key=config.get('api_key'))
        elif self.provider == 'openai':
            self.client = openai.OpenAI(api_key=config.get('api_key'))
        else:
            raise ValueError(f"Proveedor LLM no soportado: {self.provider}")

    def generate_event_summary(self, event: Dict[str, Any]) -> str:
        """
        Genera un resumen inteligente de un evento.

        Args:
            event: Diccionario de evento de Google Calendar

        Returns:
            Resumen generado por el modelo de lenguaje
        """
        try:
            prompt = self._build_event_summary_prompt(event)
            response = self._generate_text(prompt)
            return response
        except Exception as e:
            logger.error(f"Error al generar resumen de evento: {e}")
            return f"Resumen no disponible. Detalles del evento: {json.dumps(event, indent=2)}"

    def analyze_schedule(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analiza un conjunto de eventos y proporciona insights.

        Args:
            events: Lista de eventos de Google Calendar

        Returns:
            Diccionario con análisis de la agenda
        """
        try:
            prompt = self._build_schedule_analysis_prompt(events)
            response_str = self._generate_text(prompt)
            
            # Intentar parsear la respuesta como JSON
            try:
                response_json = json.loads(response_str)
                return response_json
            except json.JSONDecodeError:
                # Si no es JSON válido, devolver como texto plano
                return {
                    'analysis_text': response_str,
                    'raw_events_count': len(events)
                }
        except Exception as e:
            logger.error(f"Error al analizar agenda: {e}")
            return {
                'error': str(e),
                'raw_events_count': len(events)
            }

    def suggest_optimal_meeting_time(self, 
                                     participants: List[str], 
                                     duration: int, 
                                     constraints: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Sugiere un tiempo óptimo para una reunión.

        Args:
            participants: Lista de correos electrónicos de participantes
            duration: Duración de la reunión en minutos
            constraints: Restricciones adicionales para la programación

        Returns:
            Sugerencia de tiempo de reunión
        """
        try:
            prompt = self._build_meeting_time_prompt(participants, duration, constraints)
            response_str = self._generate_text(prompt)
            
            try:
                response_json = json.loads(response_str)
                return response_json
            except json.JSONDecodeError:
                return {
                    'suggestion_text': response_str,
                    'participants': participants,
                    'duration_minutes': duration
                }
        except Exception as e:
            logger.error(f"Error al sugerir tiempo de reunión: {e}")
            return {
                'error': str(e),
                'participants': participants,
                'duration_minutes': duration
            }

    def _generate_text(self, prompt: str) -> str:
        """
        Genera texto usando el modelo de lenguaje configurado.

        Args:
            prompt: Texto de entrada para el modelo

        Returns:
            Texto generado por el modelo
        """
        try:
            if self.provider == 'groq':
                chat_completion = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=self.model,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                return chat_completion.choices[0].message.content
            
            elif self.provider == 'openai':
                chat_completion = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=self.model,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                return chat_completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Error al generar texto con LLM: {e}")
            raise

    def _build_event_summary_prompt(self, event: Dict[str, Any]) -> str:
        """
        Construye un prompt para generar resumen de evento.

        Args:
            event: Diccionario de evento de Google Calendar

        Returns:
            Prompt para generación de resumen
        """
        return f"""
        Genera un resumen conciso y útil para el siguiente evento de calendario:

        Título: {event.get('summary', 'Sin título')}
        Hora de inicio: {event.get('start', {}).get('dateTime', 'No especificada')}
        Hora de fin: {event.get('end', {}).get('dateTime', 'No especificada')}
        Descripción: {event.get('description', 'Sin descripción')}
        Participantes: {', '.join([p.get('email', '') for p in event.get('attendees', [])])}

        El resumen debe ser informativo, claro y destacar los puntos clave del evento.
        """

    def _build_schedule_analysis_prompt(self, events: List[Dict[str, Any]]) -> str:
        """
        Construye un prompt para analizar la agenda.

        Args:
            events: Lista de eventos de Google Calendar

        Returns:
            Prompt para análisis de agenda
        """
        events_summary = "\n".join([
            f"- {event.get('summary', 'Sin título')} "
            f"({event.get('start', {}).get('dateTime', 'Sin hora')})"
            for event in events
        ])

        return f"""
        Analiza la siguiente agenda de eventos y proporciona un resumen estructurado en JSON:

        Eventos:
        {events_summary}

        El análisis debe incluir:
        1. Número total de eventos
        2. Distribución de eventos por tipo (trabajo, personal, reuniones)
        3. Tiempo total ocupado
        4. Intervalos de tiempo libre
        5. Sugerencias de optimización de agenda

        Formato de respuesta: JSON con campos descriptivos y concisos.
        """

    def _build_meeting_time_prompt(self, 
                                   participants: List[str], 
                                   duration: int, 
                                   constraints: Optional[Dict[str, Any]] = None) -> str:
        """
        Construye un prompt para sugerir tiempo de reunión.

        Args:
            participants: Lista de correos electrónicos
            duration: Duración de la reunión en minutos
            constraints: Restricciones adicionales

        Returns:
            Prompt para sugerencia de tiempo de reunión
        """
        constraints_str = json.dumps(constraints) if constraints else "Ninguna restricción específica"

        return f"""
        Sugiere un tiempo óptimo para una reunión con las siguientes características:

        Participantes: {', '.join(participants)}
        Duración: {duration} minutos
        Restricciones: {constraints_str}

        La sugerencia debe ser un objeto JSON que incluya:
        1. Fecha y hora recomendadas
        2. Justificación de la elección
        3. Consideraciones de zona horaria
        4. Posibles alternativas

        Formato de respuesta: JSON con campos descriptivos y concisos.
        """
