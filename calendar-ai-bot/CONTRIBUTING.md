# Contribución a Calendar AI Bot

## Bienvenido/a a Calendar AI Bot

¡Gracias por tu interés en contribuir a Calendar AI Bot! Este documento proporciona pautas para contribuir al proyecto.

## Configuración del Entorno de Desarrollo

### Requisitos Previos

- Python 3.9+
- pip
- virtualenv

### Configuración del Entorno

1. Clonar el repositorio
```bash
git clone https://github.com/yourusername/calendar-ai-bot.git
cd calendar-ai-bot
```

2. Crear y activar entorno virtual
```bash
./activate_venv.sh
```

3. Instalar dependencias de desarrollo
```bash
pip install -r requirements-dev.txt
```

4. Instalar pre-commit hooks
```bash
pre-commit install
```

## Flujo de Trabajo de Contribución

### 1. Crear una Rama

```bash
git checkout -b feature/nombre-de-tu-caracteristica
# o
git checkout -b bugfix/descripcion-del-bug
```

### 2. Hacer Cambios

- Sigue las mejores prácticas de Python
- Escribe código limpio y legible
- Agrega pruebas para nuevas funcionalidades
- Documenta tus cambios

### 3. Ejecutar Pruebas

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar pruebas con cobertura
pytest --cov=calendar_ai_bot tests/
```

### 4. Formatear y Verificar Código

```bash
# Formatear código
black .
isort .

# Verificar estilo de código
flake8
mypy .
```

### 5. Hacer Commit

Usamos [Commitizen](https://github.com/commitizen-tools/commitizen) para mensajes de commit:

```bash
cz commit
```

### 6. Enviar Pull Request

- Describe claramente tus cambios
- Vincula cualquier issue relacionado
- Asegúrate de que todas las verificaciones pasen

## Guías de Estilo

### Código Python

- Seguir PEP 8
- Usar type hints
- Documentar funciones y clases
- Mantener líneas bajo 100 caracteres
- Usar nombres descriptivos

### Pruebas

- Cubrir casos de éxito y error
- Usar mocks para dependencias externas
- Mantener pruebas independientes
- Documentar el propósito de cada prueba

## Proceso de Revisión

- Un revisor debe aprobar los cambios
- Todas las verificaciones de CI deben pasar
- Se requiere revisión de código
- Se pueden solicitar cambios

## Reportar Problemas

- Usa GitHub Issues
- Proporciona detalles específicos
- Incluye pasos para reproducir
- Menciona versiones de Python y dependencias

## Código de Conducta

- Sé respetuoso
- Colabora de manera constructiva
- Mantén un ambiente inclusivo

## Preguntas Frecuentes

### ¿Cómo puedo comenzar a contribuir?

- Revisa los issues etiquetados como "good first issue"
- Lee la documentación del proyecto
- Únete al canal de comunicación del proyecto

### ¿Qué tipo de contribuciones se aceptan?

- Corrección de bugs
- Mejoras de rendimiento
- Nuevas características
- Mejoras en documentación
- Correcciones de estilo de código

## Recursos Adicionales

- [Documentación del Proyecto](README.md)
- [Guía de Instalación](README.md)
- [Licencia](LICENSE)

¡Gracias por contribuir a Calendar AI Bot!
