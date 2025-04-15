# ruleta

## Descripción
Proyecto dockerizado, para correr usar:

```bash
docker-compose up -d --build
```
para detener usar:
```bash
docker-compose down --remove-orphans
```
para recompilar la imagen (Linux):
```bash
docker-compose down --remove-orphans && docker-compose up -d --build
```

## Requisitos
- Docker
- Docker Compose
- Python 3.8 o superior
- pip
- pipenv
- node