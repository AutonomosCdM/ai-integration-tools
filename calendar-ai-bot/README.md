# Calendar AI Bot

Un bot de integración de Google Calendar con capacidades de IA para la gestión inteligente de eventos y calendarios.

## Características

- Integración con Google Calendar API
- Procesamiento inteligente de eventos
- Organización automática de eventos
- Filtrado avanzado de eventos
- Asistente de programación inteligente
- Automatizaciones basadas en reglas
- Análisis de disponibilidad y conflictos

## Requisitos

- Python 3.9+
- Credenciales de Google Calendar API
- Acceso a un modelo de lenguaje (LLM)

## Instalación

1. Clonar el repositorio
2. Instalar dependencias: `pip install -r requirements.txt`
3. Configurar credenciales de Google Calendar API
4. Ejecutar `python app.py`

## Estructura del Proyecto

```
calendar-ai-bot/
├── calendar/           # Módulos de integración con Calendar
│   ├── interface.py    # Interfaz con Google Calendar API
│   ├── processor.py    # Procesamiento de eventos
│   ├── organizer.py    # Organización de eventos
│   └── filters.py      # Filtros para eventos
├── llm/                # Integración con modelos de lenguaje
│   └── client.py       # Cliente para LLM
├── utils/              # Utilidades generales
│   ├── cache.py        # Sistema de caché
│   ├── config.py       # Gestión de configuración
│   ├── context.py      # Gestión de contexto
│   └── credentials.py  # Manejo de credenciales
├── tests/              # Pruebas unitarias e integración
├── app.py              # Aplicación principal
├── requirements.txt    # Dependencias del proyecto
└── setup.py            # Configuración de instalación
```

## Uso

```python
from calendar_ai_bot import CalendarAIBot

# Inicializar el bot
bot = CalendarAIBot(config_path='config.json')

# Obtener eventos próximos
events = bot.get_upcoming_events(days=7)

# Analizar eventos
analysis = bot.analyze_events(events)

# Organizar eventos
bot.organize_events(events)

# Programar un nuevo evento
bot.schedule_optimal_meeting(
    title="Reunión de equipo",
    duration_minutes=60,
    participants=["usuario1@example.com", "usuario2@example.com"],
    preferred_days=["Lunes", "Miércoles", "Viernes"]
)
```

## Pruebas

Ejecutar pruebas unitarias:

```
python -m pytest tests/
```

## Licencia

MIT
