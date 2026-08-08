# 📋 Sistema de Tareas — Proyecto Final (Microservicios / Podman)

Aplicación web orientada a servicios para la gestión de tareas personales, desarrollada con arquitectura cliente-servidor, API REST, persistencia en PostgreSQL y despliegue mediante contenedores **Podman**.

## Descripción del problema

Muchas personas necesitan un lugar simple para registrar, priorizar y dar seguimiento a sus tareas pendientes. Este sistema permite crear, consultar, actualizar y eliminar tareas, asignarles una prioridad y un estado, y filtrarlas por estado.

## Tecnologías utilizadas

| Capa | Tecnología |
|---|---|
| Backend / API REST | Python + Flask + Flask-SQLAlchemy |
| Base de datos | PostgreSQL 16 |
| Frontend | HTML5, CSS3, JavaScript (fetch API) |
| Contenedores | Podman (Containerfile por servicio) |
| Orquestación local | podman-compose |
| Control de versiones | Git / GitHub |

## Arquitectura

```
[ Navegador ]
      │  HTTP
      ▼
[ Frontend: Nginx :8080 ]
      │  fetch() a la API REST
      ▼
[ Backend: Flask :5000 ]
      │  SQLAlchemy / psycopg2
      ▼
[ PostgreSQL :5432 ]
```

## Estructura del repositorio

```
sistema-tareas/
├── backend/
│   ├── app.py              # API REST (Flask)
│   ├── models.py           # Modelo Tarea (SQLAlchemy)
│   ├── requirements.txt
│   ├── Containerfile
│   └── .env.example
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── Containerfile
├── container/
│   └── podman-compose.yml
├── docs/
│   └── capturas/            # Screenshots de evidencia
├── README.md
└── .gitignore
```

## Modelo de datos — Tarea

| Campo | Tipo | Descripción |
|---|---|---|
| id | Integer | Identificador autogenerado |
| titulo | String(150) | Obligatorio |
| descripcion | Text | Opcional |
| estado | String | `pendiente` \| `en_proceso` \| `completada` |
| prioridad | String | `baja` \| `media` \| `alta` |
| fecha_creacion | DateTime | Autogenerada |
| fecha_limite | Date | Opcional |

## Endpoints de la API REST

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/health` | Verifica que la API está activa |
| GET | `/api/tareas` | Lista todas las tareas (filtros opcionales: `?estado=`, `?prioridad=`) |
| GET | `/api/tareas/<id>` | Obtiene una tarea por id |
| POST | `/api/tareas` | Crea una tarea |
| PUT | `/api/tareas/<id>` | Actualiza una tarea |
| DELETE | `/api/tareas/<id>` | Elimina una tarea |

### Ejemplo — crear tarea (curl)

```bash
curl -X POST http://localhost:5000/api/tareas \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Estudiar Podman", "prioridad": "alta", "estado": "pendiente"}'
```

## Cómo ejecutar el proyecto con Podman

### Requisito previo
Tener instalado `podman` y `podman-compose`:

```bash
sudo apt install podman podman-compose   # Ubuntu/Debian
brew install podman podman-compose       # macOS
```

### Opción A — con podman-compose (recomendado)

```bash
cd container
podman-compose up --build
```

Esto levanta 3 contenedores:
- `tareas-db` → PostgreSQL en el puerto 5432
- `tareas-backend` → API Flask en el puerto 5000
- `tareas-frontend` → sitio estático (Nginx) en el puerto 8080

Luego abre el navegador en: **http://localhost:8080**

Para detener y eliminar los contenedores:
```bash
podman-compose down
```

### Opción B — contenedores manuales (sin compose)

```bash
# Red compartida para que los contenedores se vean entre sí
podman network create tareas-net

# Base de datos
podman run -d --name tareas-db --network tareas-net \
  -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=tareas_db \
  -p 5432:5432 postgres:16-alpine

# Backend
podman build -t tareas-backend ./backend
podman run -d --name tareas-backend --network tareas-net \
  -e DB_HOST=tareas-db -e DB_USER=postgres -e DB_PASSWORD=postgres -e DB_NAME=tareas_db \
  -p 5000:5000 tareas-backend

# Frontend
podman build -t tareas-frontend ./frontend
podman run -d --name tareas-frontend --network tareas-net \
  -p 8080:80 tareas-frontend
```

## Pruebas realizadas

- [x] Registrar una tarea desde el formulario web.
- [x] Consultar el listado de tareas y filtrar por estado.
- [x] Editar una tarea existente.
- [x] Eliminar una tarea.
- [x] Probar los endpoints con `curl` / Postman.
- [x] Verificar que los 3 contenedores levantan correctamente con `podman ps`.
- [x] Verificar persistencia: los datos siguen ahí tras reiniciar el contenedor del backend.

## Capturas de pantalla

_(Agregar aquí imágenes desde `docs/capturas/`, por ejemplo:)_

`![Listado de tareas](docs/capturas/listado.png)`

## Autor

Nombre del estudiante — Proyecto Final, Microservicios / Aplicación Web Orientada a Servicios con Podman.
