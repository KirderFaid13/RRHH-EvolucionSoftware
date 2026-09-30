# Contexto funcional inicial

Este archivo incorpora lo observado en C02 mediante análisis estático y descompilación de ClassRRHH.dll. Una pregunta pendiente no equivale a una regla del negocio; leer código no demuestra su comportamiento con datos reales.

## Información confirmada por el equipo

- El objeto del curso es un sistema de Recursos Humanos identificado por el equipo como un sistema del año 2008.
- El proyecto final consiste en estudiar el sistema existente mediante ingeniería inversa, refactorizarlo y hacerlo evolucionar de manera gradual.
- Los avances del curso se realizan semanalmente y deben documentar el cambio relacionado con el tema de cada semana.
- El primer commit conserva la entrega original disponible y prepara una estructura que permita documentar los siguientes avances.

La fuente de estos puntos es la explicación del equipo. Las evidencias técnicas se distinguen a continuación.

## Operaciones y dependencias observadas en C02

| Elemento | Evidencia | Lo que falta verificar |
| --- | --- | --- |
| Consultas y cambios de empleados, permisos, asistencia y reportes | Métodos de `RRHHClass`, recuperados en [fuente C#](../src/v1/recuperado/ClassRRHH/RRHHClass.cs). | Flujo completo, validaciones del servidor, reglas y resultados reales. |
| Captura/importación Access | `AsistenciaAccess` utiliza OleDb/Jet y SQL; cuatro `Access2Sql*` reciben fechas y `forzar`. | Formato MDB, efectos de cada variante, duplicados y comportamiento con fallos. |
| Familiares y ficha social | `FamiliaresClass` consulta personas/parentescos; `FichaSocialClass` llama `spRRHH_BuscarFamiliares`. | Esquema, autorizaciones y alcance de los formularios. |
| Reporte por oficina | `Generar_Report_oficina` usa `spRRHH_Report_Oficina_Unico/@idarea`; la variante por sigla usa `spRRHH_Report_Oficina/@sigla`. | Existencia, firmas y salidas de los procedimientos en CMI. |
| Acceso SQL compartido | Constructores obtienen `GRLL.Common.clsConexion.Conexion`. | Ciclo de vida y comportamiento completo del proveedor y su uso por UI. |
| Interfaz de escritorio | Metadatos de Windows Forms/MainMDI y métodos BackgroundWorker en cinco formularios. | Flujo visible y ejecución real; no se recuperó toda la interfaz. |

Fuentes: [arquitectura](../docs/ingenieria_inversa/02_arquitectura.md), [contratos observados](../evidencia/ingenieria_inversa/contratos_observados.json) y [metadatos](../evidencia/ingenieria_inversa/ensamblados_propios.json). La v1 previa era una reconstrucción parcial; [auditoría](../docs/ingenieria_inversa/04_revision_antecedente.md).

## Información funcional pendiente

| Aspecto | Estado inicial | Evidencia que necesitamos |
| --- | --- | --- |
| Usuarios y roles | Desconocidos | Pantallas, código recuperado o documentación del sistema. |
| Permisos por rol | Desconocidos | Reglas verificables de autorización. |
| Módulos y operaciones | Parcialmente recuperados mediante código/metadatos | Completar inventario de pantallas y rutas de ejecución. |
| Flujos de Recursos Humanos | Desconocidos | Secuencias de entrada, validación, persistencia y resultado. |
| Validaciones y restricciones | Desconocidas | Código, mensajes del sistema y restricciones de datos. |
| Integraciones y dependencias | SQL Server/SqlClient, OleDb/Jet, GRLL, Seguridad y UI observados | Verificar instalaciones, rutas y operación real. |

No se define todavía una matriz de permisos: asignar capacidades a roles supuestos produciría un contexto ficticio. Cuando se encuentren roles y operaciones reales, se registrará cada permiso junto con su evidencia y sus dudas pendientes.

## Criterios para incorporar reglas

1. Citar el archivo, pantalla o artefacto que sustenta la regla.
2. Distinguir lo observado de una interpretación o propuesta.
3. Explicar las condiciones de entrada y el resultado esperado cuando haya evidencia suficiente.
4. Registrar cualquier diferencia entre la documentación y el comportamiento observado.
5. Mantener visible lo que todavía no se pudo verificar.

La refactorización debe preservar el comportamiento comprobado del sistema. Cualquier modificación de ese comportamiento requiere una decisión explícita y una explicación en la documentación del cambio.

Consulta el [contexto del curso](03_course_context.md) y el [roadmap](ROADMAP.md) para conocer el orden de trabajo.
