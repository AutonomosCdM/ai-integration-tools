# Pruebas de Calendar AI Bot

## Estructura de Pruebas

Este directorio contiene pruebas unitarias e integración para el Calendar AI Bot.

### Categorías de Pruebas

- `test_interface.py`: Pruebas para la interfaz de Google Calendar
- `test_processor.py`: Pruebas para procesamiento de eventos
- `test_organizer.py`: Pruebas para organización de eventos
- `test_filters.py`: Pruebas para filtrado de eventos
- `test_llm_client.py`: Pruebas para el cliente de Modelo de Lenguaje
- `test_config.py`: Pruebas para gestión de configuración
- `test_credentials.py`: Pruebas para manejo de credenciales
- `test_cache.py`: Pruebas para sistema de caché
- `test_context.py`: Pruebas para gestión de contexto

## Ejecución de Pruebas

Para ejecutar todas las pruebas:

```bash
python -m pytest
```

Para ejecutar pruebas específicas:

```bash
python -m pytest tests/test_interface.py
```

## Configuración de Pruebas

### Requisitos

- pytest
- pytest-mock
- pytest-cov

### Instalación de Dependencias

```bash
pip install -r requirements-dev.txt
```

## Cobertura de Código

Para generar un informe de cobertura de código:

```bash
python -m pytest --cov=calendar_ai_bot tests/
```

## Mejores Prácticas

1. Cada módulo debe tener pruebas unitarias exhaustivas
2. Usar mocks para simular dependencias externas
3. Cubrir casos de éxito y casos de error
4. Mantener las pruebas independientes y aisladas
5. Documentar claramente el propósito de cada prueba

## Configuración de Entorno de Pruebas

- Usar variables de entorno para configuraciones sensibles
- Crear archivos de configuración de pruebas separados
- Simular credenciales y tokens para pruebas de API
