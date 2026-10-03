# v4.0 - Refactorización DIP/IoC (Semana 07)

## Descripción
Refactorización del sistema RRHH aplicando el **Principio de Inversión de Dependencias (DIP)** y el patrón de **Inversión de Control (IoC)**.

## Cambios clave respecto a v3.0
1. 4 nuevas interfaces: `IDatabaseHelper`, `IEmpleadoRepository`, `IAsistenciaRepository`, `IPermisoRepository`
2. Todas las clases implementan interfaces y dependen de abstracciones (no concretos)
3. `ServiceContainer` — contenedor IoC didáctico
4. `CompositionRoot` — único lugar con `new` en toda la aplicación
