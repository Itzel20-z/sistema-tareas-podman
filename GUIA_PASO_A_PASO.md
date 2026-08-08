# Guía paso a paso — Sistema de Tareas (Flask + PostgreSQL + Podman)

Esta guía te lleva desde cero hasta la entrega final. Ya te generé el código base (backend, frontend, contenedores). Aquí aprendes a levantarlo, probarlo, subirlo a GitHub y documentarlo.

---

## 0. Requisitos previos

Instala en tu máquina:

1. **Git** → `sudo apt install git` (Linux) o descárgalo de git-scm.com
2. **Podman** y **podman-compose**:
   ```bash
   sudo apt update
   sudo apt install podman podman-compose
   ```
   En macOS: `brew install podman podman-compose` y luego `podman machine init && podman machine start`
   En Windows: instala Podman Desktop.
3. Verifica instalación:
   ```bash
   podman --version
   podman-compose --version
   git --version
   ```
4. (Opcional, para probar sin contenedores) **Python 3.11+** instalado localmente.

---

## 1. Descarga y organiza el proyecto

Ya tienes la carpeta `sistema-tareas/` con esta estructura:

```
sistema-tareas/
├── backend/        (API Flask + modelo Tarea)
├── frontend/        (HTML/CSS/JS)
├── container/        (podman-compose.yml)
├── docs/             (aquí van tus capturas)
├── README.md
├── GUIA_PASO_A_PASO.md
└── .gitignore
```

Copia esta carpeta a tu computadora y ábrela en tu editor (VS Code recomendado).

---

## 2. Crea el repositorio en GitHub

1. Entra a github.com → botón **New repository**.
2. Nómbralo, por ejemplo: `sistema-tareas-podman`.
3. NO marques "Add README" (ya tienes uno).
4. Crea el repo y copia la URL (ej. `https://github.com/tu-usuario/sistema-tareas-podman.git`).
5. En tu terminal, dentro de la carpeta del proyecto:
   ```bash
   git init
   git add .
   git commit -m "Estructura inicial del proyecto: backend, frontend y contenedores"
   git branch -M main
   git remote add origin https://github.com/tu-usuario/sistema-tareas-podman.git
   git push -u origin main
   ```

A partir de aquí, haz **commits frecuentes** con mensajes claros cada vez que avances (ej. `git commit -m "Agrega endpoint DELETE de tareas"`).

---

## 3. Levanta los contenedores con Podman

Desde la raíz del proyecto:

```bash
cd container
podman-compose up --build
```

Qué pasa internamente:
- Se construye la imagen del **backend** (Python + Flask) a partir de `backend/Containerfile`.
- Se construye la imagen del **frontend** (Nginx sirviendo HTML/CSS/JS) a partir de `frontend/Containerfile`.
- Se descarga la imagen oficial de **PostgreSQL 16**.
- Se crean 3 contenedores conectados en la misma red: `tareas-db`, `tareas-backend`, `tareas-frontend`.
- Flask crea automáticamente la tabla `tareas` en PostgreSQL al iniciar (línea `db.create_all()` en `app.py`).

Verifica que los 3 contenedores están corriendo:
```bash
podman ps
```

Deberías ver `tareas-db`, `tareas-backend` y `tareas-frontend` con estado "Up".

---

## 4. Prueba que todo funciona

### 4.1 Prueba la API directamente
```bash
curl http://localhost:5000/api/health
# Debe responder: {"status": "ok"}

curl -X POST http://localhost:5000/api/tareas \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Probar API", "prioridad": "alta"}'

curl http://localhost:5000/api/tareas
```

### 4.2 Prueba el frontend
Abre en tu navegador: **http://localhost:8080**

- Registra una tarea desde el formulario.
- Verifica que aparece en la tabla.
- Edítala (botón "Editar") y guarda los cambios.
- Elimínala (botón "Eliminar").
- Prueba el filtro por estado.

### 4.3 Prueba de persistencia
```bash
podman restart tareas-backend
```
Recarga el navegador: las tareas siguen ahí porque están en PostgreSQL, no en memoria.

### 4.4 Revisa los logs si algo falla
```bash
podman logs tareas-backend
podman logs tareas-db
podman logs tareas-frontend
```

---

## 5. Toma las evidencias (capturas y video)

Crea la carpeta `docs/capturas/` y guarda ahí:
1. Captura de `podman ps` mostrando los 3 contenedores activos.
2. Captura del frontend con al menos 3 tareas registradas (distintos estados/prioridades).
3. Captura de una petición exitosa con `curl` o Postman.
4. Captura del código de un endpoint (por ejemplo `app.py`).
5. Un video corto (2-4 min) grabando tu pantalla mientras: levantas los contenedores, creas una tarea, la editas, la eliminas, y explicas brevemente la arquitectura. Puedes usar OBS Studio, el grabador de pantalla de Windows/Mac, o Loom.

Sube el video a YouTube (no listado) o Google Drive y agrega el link al README.

---

## 6. Completa la documentación

Edita `README.md` (ya tiene la mayoría del contenido) y asegúrate de incluir:
- [x] Descripción del problema y la solución.
- [x] Tecnologías usadas.
- [x] Estructura del repo.
- [x] Instrucciones exactas de ejecución con Podman.
- [x] Endpoints de la API.
- [ ] Capturas de pantalla (agrégalas tú con tus pruebas reales).
- [ ] Link al video demo.
- [ ] Tu nombre.

---

## 7. Checklist final antes de entregar

- [ ] El repo es público (o compartido con el profesor) y todo el código está subido.
- [ ] `podman-compose up --build` levanta el proyecto sin errores desde cero.
- [ ] Los 4 CRUD funcionan (crear, leer, actualizar, eliminar) desde el frontend.
- [ ] La API responde correctamente a `curl`/Postman.
- [ ] Los datos persisten después de reiniciar contenedores.
- [ ] README completo con instrucciones claras.
- [ ] Capturas de pantalla en `docs/capturas/`.
- [ ] Video demo enlazado.
- [ ] Historial de commits con mensajes descriptivos (no un solo commit gigante).
- [ ] Revisaste que no subiste contraseñas reales (usa `.env`, que está en `.gitignore`).

---

## 8. Mapeo con las fases del proyecto

| Fase del proyecto | Ya cubierto por este material |
|---|---|
| Fase 1: Planeación | Problema y alcance definidos en el README |
| Fase 2: Diseño | Modelo de datos, endpoints y arquitectura documentados |
| Fase 3: Implementación | Backend, frontend y contenedores ya generados — tú los ejecutas y ajustas |
| Fase 4: Pruebas | Sección 4 de esta guía |
| Fase 5: Entrega | Secciones 5, 6 y 7 de esta guía |

---

## 9. Ideas para extender (opcional, si quieres puntos extra)

- Agregar autenticación simple (usuario/contraseña) para que cada quien vea solo sus tareas.
- Agregar categorías o etiquetas a las tareas.
- Ordenar tareas por fecha límite próxima.
- Agregar tests automatizados con `pytest` para los endpoints.
- Agregar un `Makefile` con atajos (`make up`, `make down`, `make logs`).

---

Con esto tienes todo el flujo cubierto: código funcional, contenedores, y el proceso exacto de documentación y entrega. Si algún paso te da un error específico (por ejemplo, algo en `podman-compose up`), pégame el mensaje de error y lo resolvemos juntos.
