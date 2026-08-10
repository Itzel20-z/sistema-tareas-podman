Este documento registra las pruebas realizadas sobre el Sistema de Tareas para validar su correcto funcionamiento.

1. Pruebas de la API REST (CRUD completo)
Prueba	Comando	Resultado esperado	Estado
Health check	curl http://localhost:5000/api/health	{"status":"ok"}	✅ ![alt text](image.png)

Listar tareas	curl http://localhost:5000/api/tareas	Arreglo JSON con tareas	✅ ![alt text](image-1.png)

Crear tarea	curl -X POST .../api/tareas -d '{"titulo":"Prueba","prioridad":"alta"}'	Tarea creada con id nuevo (201)	✅ ![alt text](image-2.png)

Actualizar tarea	curl -X PUT .../api/tareas/1 -d '{"estado":"en_proceso"}'	Tarea actualizada (200)	✅ ![alt text](image-3.png)

Eliminar tarea	curl -X DELETE .../api/tareas/1	Mensaje de confirmación (200)	✅![alt text](image-4.png)

Tarea inexistente	curl http://localhost:5000/api/tareas/9999	{"error":"Tarea no encontrada"} (404)	✅ ![alt text](image-5.png)


2. Pruebas del frontend
Prueba	Acción	Resultado esperado	Estado
Crear tarea	Llenar formulario y guardar	Tarea aparece en la tabla	✅ ![alt text](image-6.png)

Editar tarea	Botón "Editar", cambiar datos, guardar	Tabla refleja el cambio	✅ ![alt text](image-7.png)

Eliminar tarea	Botón "Eliminar", confirmar	Tarea desaparece de la tabla	✅ ![alt text](image-8.png) ![alt text](image-9.png)

Filtro por estado	Cambiar el select de estado	Solo muestra tareas de ese estado	✅ ![alt text](image-10.png) ![alt text](image-11.png) ![alt text](image-12.png)



3. Pruebas de contenedores Podman
Prueba	Comando	Resultado esperado	Estado
Contenedores activos	podman ps	tareas-db, tareas-backend, tareas-frontend en estado "Up"	✅ ![alt text](image-13.png)

