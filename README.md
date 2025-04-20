# ruleta 2.0
Ruleta 2.0 es un proyecto que consiste en una implementación web mejorada de las ruletas genéricas disponibles en internet. Este sistema tiene como objetivo principal automatizar y optimizar el proceso de asignación de incidencias categorizadas, proporcionando una solución eficiente y accesible para el ámbito académico, específicamente en el ramo de Gestión de Proyectos Tecnológicos de la Universidad de Talca.

## Características clave
- **Gestión de incidencias**: Organización de incidencias por categorías y registro de sorteos semanales.
- **Base de datos centralizada**: Almacenamiento de los resultados de los sorteos, incluyendo el mensaje asociado a cada asignación.
- **Interfaz web**: Visualización de los sorteos y sus resultados de los sorteos, incluyendo el mensaje asociado a cada asignación.
- **Flujo semanal automatizado**: Simplificación del proceso de asignación de indcidencias y penitencias, sin necesidad de gestionar grupos o usuarios complejos.

## Requisitos para correr
- Docker
- Docker Compose
- Python 3.8 o superior
- pip
- pipenv
- node
## Como correr el proyecto
Se asumira que se tiene acceso al repositorio y github cli para la ejecución
de este item.
1. Clonar el repositorio:
```bash
gh repo clone ktax06/ruleta
```
2. Entrar al directorio del proyecto:
```bash
cd ruleta
```
3. Correr
```bash
docker-compose up -d --build
```
4. para detener usar:
```bash
docker-compose down --remove-orphans
```
5. para recompilar la imagen (Linux):
```bash
docker-compose down --remove-orphans && docker-compose up -d --build
```
