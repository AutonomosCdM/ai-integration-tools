# Configuración de Credenciales para Calendar AI Bot

Este documento detalla el proceso para configurar las credenciales necesarias para que el Calendar AI Bot pueda interactuar con la API de Google Calendar.

## Requisitos Previos

1. Cuenta de Google
2. Acceso a Google Cloud Console
3. Proyecto creado en Google Cloud

## Paso 1: Crear un Proyecto en Google Cloud Console

1. Accede a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Anota el ID del proyecto para referencia futura

## Paso 2: Habilitar la API de Google Calendar

1. En el menú lateral, navega a "APIs y Servicios" > "Biblioteca"
2. Busca "Google Calendar API"
3. Selecciona la API y haz clic en "Habilitar"

## Paso 3: Configurar la Pantalla de Consentimiento OAuth

1. En el menú lateral, navega a "APIs y Servicios" > "Pantalla de consentimiento de OAuth"
2. Selecciona el tipo de usuario (externo o interno)
3. Completa la información requerida:
   - Nombre de la aplicación
   - Correo electrónico de soporte
   - Dominios autorizados
4. Añade los siguientes ámbitos:
   - `https://www.googleapis.com/auth/calendar`
   - `https://www.googleapis.com/auth/calendar.events`
5. Añade usuarios de prueba si es necesario
6. Completa el proceso de configuración

## Paso 4: Crear Credenciales OAuth

1. En el menú lateral, navega a "APIs y Servicios" > "Credenciales"
2. Haz clic en "Crear Credenciales" y selecciona "ID de cliente de OAuth"
3. Selecciona "Aplicación de escritorio" como tipo de aplicación
4. Asigna un nombre a la aplicación (ej. "Calendar AI Bot")
5. Haz clic en "Crear"
6. Descarga el archivo JSON de credenciales

## Paso 5: Configurar el Bot

1. Renombra el archivo descargado a `calendar_credentials.json`
2. Coloca el archivo en el directorio raíz del proyecto o en la ubicación especificada en `config.json`
3. La primera vez que ejecutes el bot, se abrirá un navegador para autorizar el acceso
4. Después de autorizar, se generará un archivo `calendar_token.json` que contiene el token de acceso

## Estructura de Archivos

```
calendar-ai-bot/
├── calendar_credentials.json  # Credenciales de OAuth (descargadas de Google Cloud)
├── calendar_token.json        # Token de acceso (generado automáticamente)
└── config.json                # Configuración del bot (incluye rutas a los archivos de credenciales)
```

## Consideraciones de Seguridad

- Nunca compartas o subas a repositorios públicos los archivos `calendar_credentials.json` o `calendar_token.json`
- Añade estos archivos a `.gitignore`
- Para entornos de producción, considera usar variables de entorno o servicios de gestión de secretos
- Revisa periódicamente los permisos y accesos concedidos en la consola de Google Cloud

## Solución de Problemas

### Error de Autenticación

Si encuentras errores de autenticación:

1. Verifica que los archivos de credenciales estén en la ubicación correcta
2. Asegúrate de que la API de Calendar esté habilitada en tu proyecto
3. Comprueba que los ámbitos solicitados sean correctos
4. Elimina el archivo `calendar_token.json` y vuelve a autorizar la aplicación

### Error de Permisos

Si encuentras errores de permisos:

1. Verifica que los ámbitos solicitados incluyan los permisos necesarios
2. Comprueba que el usuario haya aceptado todos los permisos durante la autorización
3. Revisa la configuración de la pantalla de consentimiento OAuth

## Referencias

- [Documentación de Google Calendar API](https://developers.google.com/calendar/api/guides/overview)
- [Guía de Autenticación de Google](https://developers.google.com/identity/protocols/oauth2)
- [Biblioteca de Cliente de Google para Python](https://github.com/googleapis/google-api-python-client)
