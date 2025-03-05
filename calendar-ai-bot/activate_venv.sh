#!/bin/bash

# Nombre del entorno virtual
VENV_NAME="calendar_ai_bot_venv"

# Función para crear el entorno virtual si no existe
create_venv() {
    if [ ! -d "$VENV_NAME" ]; then
        echo "Creando entorno virtual..."
        python3 -m venv "$VENV_NAME"
    fi
}

# Función para activar el entorno virtual
activate_venv() {
    # Activar el entorno virtual
    source "$VENV_NAME/bin/activate"
    echo "Entorno virtual $VENV_NAME activado"
}

# Función para instalar dependencias
install_dependencies() {
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
}

# Función principal
main() {
    # Cambiar al directorio del script
    cd "$(dirname "$0")"

    # Crear entorno virtual
    create_venv

    # Activar entorno virtual
    activate_venv

    # Instalar dependencias
    install_dependencies

    # Mostrar información del entorno
    python --version
    pip list
}

# Ejecutar función principal
main
