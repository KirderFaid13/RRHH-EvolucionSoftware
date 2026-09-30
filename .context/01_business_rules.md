# Contexto funcional inicial

Este archivo registra lo que sabemos al incorporar el RRHH original al repositorio. Se actualizará mediante commits cuando la ingeniería inversa aporte evidencia. Una pregunta pendiente no equivale a una regla del negocio.

## Información confirmada por el equipo

- El objeto del curso es un sistema de Recursos Humanos identificado por el equipo como un sistema del año 2008.
- El proyecto final consiste en estudiar el sistema existente mediante ingeniería inversa, refactorizarlo y hacerlo evolucionar de manera gradual.
- Los avances del curso se realizan semanalmente y deben documentar el cambio relacionado con el tema de cada semana.
- El primer commit conserva la entrega original disponible y prepara una estructura que permita documentar los siguientes avances.

La fuente de estos puntos es la explicación del equipo. Todavía no representan una validación técnica del código, de los binarios ni de la base de datos.

## Información funcional pendiente

| Aspecto | Estado inicial | Evidencia que necesitamos |
| --- | --- | --- |
| Usuarios y roles | Desconocidos | Pantallas, código recuperado o documentación del sistema. |
| Permisos por rol | Desconocidos | Reglas verificables de autorización. |
| Módulos y operaciones | Desconocidos | Inventario de pantallas y rutas de ejecución. |
| Flujos de Recursos Humanos | Desconocidos | Secuencias de entrada, validación, persistencia y resultado. |
| Validaciones y restricciones | Desconocidas | Código, mensajes del sistema y restricciones de datos. |
| Integraciones y dependencias | Desconocidas | Configuraciones y referencias técnicas verificadas. |

No se define todavía una matriz de permisos: asignar capacidades a roles supuestos produciría un contexto ficticio. Cuando se encuentren roles y operaciones reales, se registrará cada permiso junto con su evidencia y sus dudas pendientes.

## Criterios para incorporar reglas

1. Citar el archivo, pantalla o artefacto que sustenta la regla.
2. Distinguir lo observado de una interpretación o propuesta.
3. Explicar las condiciones de entrada y el resultado esperado cuando haya evidencia suficiente.
4. Registrar cualquier diferencia entre la documentación y el comportamiento observado.
5. Mantener visible lo que todavía no se pudo verificar.

La refactorización debe preservar el comportamiento comprobado del sistema. Cualquier modificación de ese comportamiento requiere una decisión explícita y una explicación en la documentación del cambio.

Consulta el [contexto del curso](03_course_context.md) y el [roadmap](ROADMAP.md) para conocer el orden de trabajo.
