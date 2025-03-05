"""
Módulo de caché para Calendar AI Bot.
"""

import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, TypeVar, Generic, List

logger = logging.getLogger(__name__)

T = TypeVar('T')

class ResponseCache(Generic[T]):
    """
    Implementación de caché genérico con soporte para persistencia.
    """

    def __init__(self, 
                 cache_file: str = 'response_cache.json', 
                 max_size: int = 100, 
                 ttl_seconds: int = 3600):
        """
        Inicializa el caché.

        Args:
            cache_file: Ruta del archivo de caché
            max_size: Número máximo de entradas en caché
            ttl_seconds: Tiempo de vida de las entradas en caché
        """
        self.cache_file = cache_file
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache: Dict[str, Dict[str, Any]] = self._load_cache()

    def _load_cache(self) -> Dict[str, Dict[str, Any]]:
        """
        Carga el caché desde un archivo JSON.

        Returns:
            Diccionario de caché cargado
        """
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                    # Limpiar entradas caducadas
                    return {k: v for k, v in cache.items() if not self._is_expired(v)}
            return {}
        except Exception as e:
            logger.error(f"Error al cargar caché: {e}")
            return {}

    def _save_cache(self) -> None:
        """
        Guarda el caché en un archivo JSON.
        """
        try:
            # Limpiar entradas caducadas antes de guardar
            cleaned_cache = {k: v for k, v in self.cache.items() if not self._is_expired(v)}
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cleaned_cache, f, indent=2)
        except Exception as e:
            logger.error(f"Error al guardar caché: {e}")

    def _is_expired(self, cache_entry: Dict[str, Any]) -> bool:
        """
        Verifica si una entrada de caché ha expirado.

        Args:
            cache_entry: Entrada de caché a verificar

        Returns:
            True si la entrada ha expirado, False en caso contrario
        """
        try:
            timestamp = cache_entry.get('timestamp')
            if not timestamp:
                return True
            
            entry_age = datetime.now() - datetime.fromisoformat(timestamp)
            return entry_age > timedelta(seconds=self.ttl_seconds)
        except Exception as e:
            logger.error(f"Error al verificar expiración de caché: {e}")
            return True

    def _generate_cache_key(self, *args, **kwargs) -> str:
        """
        Genera una clave de caché única basada en argumentos.

        Args:
            *args: Argumentos posicionales
            **kwargs: Argumentos de palabras clave

        Returns:
            Clave de caché generada
        """
        try:
            # Convertir argumentos a cadenas y concatenarlos
            key_parts = [str(arg) for arg in args]
            key_parts.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])
            return hash(tuple(key_parts))
        except Exception as e:
            logger.error(f"Error al generar clave de caché: {e}")
            return hash(str(args) + str(kwargs))

    def get(self, *args, **kwargs) -> Optional[T]:
        """
        Obtiene una entrada de caché.

        Args:
            *args: Argumentos para generar la clave de caché
            **kwargs: Argumentos de palabras clave para generar la clave de caché

        Returns:
            Valor en caché o None si no existe o ha expirado
        """
        try:
            key = str(self._generate_cache_key(*args, **kwargs))
            
            # Verificar si la entrada existe y no ha expirado
            if key in self.cache and not self._is_expired(self.cache[key]):
                return self.cache[key]['value']
            
            return None
        except Exception as e:
            logger.error(f"Error al obtener entrada de caché: {e}")
            return None

    def set(self, value: T, *args, **kwargs) -> None:
        """
        Establece una entrada en caché.

        Args:
            value: Valor a almacenar
            *args: Argumentos para generar la clave de caché
            **kwargs: Argumentos de palabras clave para generar la clave de caché
        """
        try:
            # Limpiar entradas caducadas
            self.cache = {k: v for k, v in self.cache.items() if not self._is_expired(v)}
            
            # Verificar límite de tamaño
            if len(self.cache) >= self.max_size:
                # Eliminar la entrada más antigua
                oldest_key = min(self.cache, key=lambda k: self.cache[k].get('timestamp', ''))
                del self.cache[oldest_key]
            
            # Generar clave y crear entrada de caché
            key = str(self._generate_cache_key(*args, **kwargs))
            self.cache[key] = {
                'value': value,
                'timestamp': datetime.now().isoformat()
            }
            
            # Guardar caché
            self._save_cache()
        except Exception as e:
            logger.error(f"Error al establecer entrada de caché: {e}")

    def clear(self) -> None:
        """
        Limpia completamente el caché.
        """
        try:
            self.cache.clear()
            if os.path.exists(self.cache_file):
                os.remove(self.cache_file)
        except Exception as e:
            logger.error(f"Error al limpiar caché: {e}")

    def __len__(self) -> int:
        """
        Obtiene el número de entradas en caché.

        Returns:
            Número de entradas en caché
        """
        return len(self.cache)
