"""
Módulo de gestión de configuración para Calendar AI Bot.
"""

import json
import logging
import os
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ConfigManager:
    """
    Gestiona la configuración de la aplicación.
    """

    def __init__(self, config_path: str = 'config.json'):
        """
        Inicializa el gestor de configuración.

        Args:
            config_path: Ruta al archivo de configuración
        """
        self.config_path = config_path
        self.config: Dict[str, Any] = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Carga la configuración desde un archivo JSON.

        Returns:
            Diccionario de configuración
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logger.info(f"Configuración cargada desde {self.config_path}")
                return config
            else:
                logger.warning(f"Archivo de configuración no encontrado: {self.config_path}")
                return self._create_default_config()
        except json.JSONDecodeError:
            logger.error(f"Error al decodificar JSON en {self.config_path}")
            return self._create_default_config()
        except Exception as e:
            logger.error(f"Error al cargar configuración: {e}")
            return self._create_default_config()

    def _create_default_config(self) -> Dict[str, Any]:
        """
        Crea una configuración predeterminada.

        Returns:
            Diccionario de configuración predeterminada
        """
        default_config = {
            "app_config": {
                "name": "calendar-ai-bot",
                "version": "0.1.0",
                "log_level": "INFO",
                "polling_interval_seconds": 300
            },
            "calendar_config": {
                "scopes": [
                    "https://www.googleapis.com/auth/calendar",
                    "https://www.googleapis.com/auth/calendar.events"
                ],
                "credentials_file": "calendar_credentials.json",
                "token_file": "calendar_token.json",
                "max_results": 100,
                "timezone": "America/Santiago"
            },
            "llm_config": {
                "provider": "groq",
                "model": "llama3-70b-8192",
                "temperature": 0.7,
                "max_tokens": 1024,
                "api_key": None
            },
            "cache_config": {
                "enabled": True,
                "max_size": 100,
                "ttl_seconds": 3600,
                "cache_file": "response_cache.json"
            },
            "event_processing": {
                "analyze_content": True,
                "detect_conflicts": True,
                "process_recurring_events": True,
                "max_lookback_days": 7,
                "max_lookahead_days": 30
            },
            "organization_rules": {
                "enabled": True,
                "categorize_by_title": True,
                "categorize_by_participants": True,
                "optimize_schedule": True
            },
            "automation_rules": {
                "enabled": False,
                "send_notifications": False,
                "auto_schedule_meetings": False,
                "auto_decline_conflicts": False
            }
        }
        return default_config

    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de configuración.

        Args:
            key: Clave de configuración (puede ser anidada con puntos)
            default: Valor predeterminado si la clave no existe

        Returns:
            Valor de configuración o valor predeterminado
        """
        try:
            keys = key.split('.')
            value = self.config
            for k in keys:
                value = value.get(k, {})
            
            return value if value != {} else default
        except Exception as e:
            logger.error(f"Error al obtener configuración para {key}: {e}")
            return default

    def set(self, key: str, value: Any) -> None:
        """
        Establece un valor de configuración.

        Args:
            key: Clave de configuración (puede ser anidada con puntos)
            value: Valor a establecer
        """
        try:
            keys = key.split('.')
            config_section = self.config
            
            # Navegar hasta el último nivel
            for k in keys[:-1]:
                if k not in config_section:
                    config_section[k] = {}
                config_section = config_section[k]
            
            # Establecer el valor
            config_section[keys[-1]] = value
            
            # Guardar configuración
            self.save()
        except Exception as e:
            logger.error(f"Error al establecer configuración para {key}: {e}")

    def save(self, path: Optional[str] = None) -> None:
        """
        Guarda la configuración en un archivo.

        Args:
            path: Ruta opcional para guardar la configuración
        """
        try:
            save_path = path or self.config_path
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Configuración guardada en {save_path}")
        except Exception as e:
            logger.error(f"Error al guardar configuración: {e}")

    def validate_config(self) -> bool:
        """
        Valida la configuración actual.

        Returns:
            True si la configuración es válida, False en caso contrario
        """
        try:
            # Verificar configuraciones críticas
            required_keys = [
                'app_config.name',
                'calendar_config.credentials_file',
                'calendar_config.token_file',
                'llm_config.provider',
                'llm_config.model'
            ]
            
            for key in required_keys:
                if not self.get(key):
                    logger.error(f"Configuración faltante o inválida: {key}")
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Error al validar configuración: {e}")
            return False

    def reload(self) -> None:
        """
        Recarga la configuración desde el archivo.
        """
        try:
            self.config = self._load_config()
            logger.info("Configuración recargada")
        except Exception as e:
            logger.error(f"Error al recargar configuración: {e}")
