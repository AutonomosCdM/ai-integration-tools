"""
Módulo de gestión de credenciales para Calendar AI Bot.
"""

import json
import logging
import os
from typing import Dict, Any, Optional

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

logger = logging.getLogger(__name__)

class CredentialsManager:
    """
    Gestiona credenciales y tokens para Google Calendar API.
    """

    def __init__(self, 
                 credentials_path: str = 'calendar_credentials.json', 
                 token_path: str = 'calendar_token.json',
                 scopes: Optional[list] = None):
        """
        Inicializa el gestor de credenciales.

        Args:
            credentials_path: Ruta al archivo de credenciales OAuth
            token_path: Ruta al archivo de token de acceso
            scopes: Ámbitos de acceso para la API de Google Calendar
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.scopes = scopes or [
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/calendar.events'
        ]
        
        self.credentials = self._load_credentials()

    def _load_credentials(self) -> Optional[Credentials]:
        """
        Carga las credenciales, refrescándolas si es necesario.

        Returns:
            Objeto de credenciales de Google o None
        """
        try:
            # Intentar cargar token existente
            if os.path.exists(self.token_path):
                credentials = Credentials.from_authorized_user_file(
                    self.token_path, 
                    self.scopes
                )
                
                # Refrescar token si está caducado
                if credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
                    self._save_credentials(credentials)
                
                return credentials
            
            return None
        except Exception as e:
            logger.error(f"Error al cargar credenciales: {e}")
            return None

    def _save_credentials(self, credentials: Credentials) -> None:
        """
        Guarda las credenciales en un archivo.

        Args:
            credentials: Objeto de credenciales de Google
        """
        try:
            with open(self.token_path, 'w', encoding='utf-8') as token_file:
                token_file.write(credentials.to_json())
            logger.info("Credenciales guardadas exitosamente")
        except Exception as e:
            logger.error(f"Error al guardar credenciales: {e}")

    def authenticate(self) -> Optional[Credentials]:
        """
        Realiza el proceso de autenticación OAuth.

        Returns:
            Objeto de credenciales de Google o None
        """
        try:
            # Verificar si ya hay credenciales válidas
            if self.credentials:
                return self.credentials

            # Verificar existencia de archivo de credenciales
            if not os.path.exists(self.credentials_path):
                logger.error(f"Archivo de credenciales no encontrado: {self.credentials_path}")
                return None

            # Iniciar flujo de autenticación
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_path, 
                self.scopes
            )
            
            # Ejecutar flujo de autorización
            credentials = flow.run_local_server(port=0)
            
            # Guardar credenciales
            self._save_credentials(credentials)
            
            return credentials
        except Exception as e:
            logger.error(f"Error durante la autenticación: {e}")
            return None

    def revoke_credentials(self) -> bool:
        """
        Revoca y elimina las credenciales almacenadas.

        Returns:
            True si las credenciales fueron revocadas exitosamente, False en caso contrario
        """
        try:
            # Revocar token si existe
            if self.credentials:
                self.credentials.revoke(Request())
            
            # Eliminar archivos de token
            if os.path.exists(self.token_path):
                os.remove(self.token_path)
            
            logger.info("Credenciales revocadas y eliminadas")
            return True
        except Exception as e:
            logger.error(f"Error al revocar credenciales: {e}")
            return False

    def validate_credentials(self) -> bool:
        """
        Valida las credenciales actuales.

        Returns:
            True si las credenciales son válidas, False en caso contrario
        """
        try:
            # Verificar si hay credenciales
            if not self.credentials:
                return False
            
            # Verificar si las credenciales están caducadas
            if self.credentials.expired:
                return False
            
            # Intentar refrescar token
            if self.credentials.refresh_token:
                self.credentials.refresh(Request())
                self._save_credentials(self.credentials)
            
            return True
        except Exception as e:
            logger.error(f"Error al validar credenciales: {e}")
            return False

    def get_credentials(self) -> Optional[Credentials]:
        """
        Obtiene las credenciales, autenticándose si es necesario.

        Returns:
            Objeto de credenciales de Google o None
        """
        if not self.validate_credentials():
            return self.authenticate()
        return self.credentials

    def update_scopes(self, new_scopes: list) -> Optional[Credentials]:
        """
        Actualiza los ámbitos de las credenciales.

        Args:
            new_scopes: Nueva lista de ámbitos

        Returns:
            Objeto de credenciales actualizadas o None
        """
        try:
            self.scopes = new_scopes
            
            # Forzar nueva autenticación con nuevos ámbitos
            self.credentials = None
            return self.authenticate()
        except Exception as e:
            logger.error(f"Error al actualizar ámbitos: {e}")
            return None
