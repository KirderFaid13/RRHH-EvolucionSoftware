# v2.0 - Refactorización SRP + DRY (Semana 04)

## Descripción
Refactorización del sistema legado RRHH aplicando el **Principio de Responsabilidad Única (SRP)** y el principio **DRY (Don't Repeat Yourself)**. La clase monolítica `ClassRRHH` (+20 métodos, múltiples responsabilidades) se descompone en 6 clases especializadas.

## Principios Aplicados

### SRP — Single Responsibility Principle
> "Una clase debe tener una, y solo una, razón para cambiar."

**Antes:** `ClassRRHH.vb` manejaba empleados, asistencias, permisos, reportes e importaciones en una sola clase.  
**Después:** Cada clase tiene una única responsabilidad claramente definida.

### DRY — Don't Repeat Yourself
> "Cada pieza de conocimiento debe tener una representación única, inequívoca y autoritativa dentro del sistema."

**Antes:** 15+ bloques de conexión a BD repetidos y 4 métodos `Access2Sql*` casi idénticos (~120 líneas duplicadas).  
**Después:** Un solo `DatabaseHelper` centraliza la conexión y un solo `ImportarDesdeAccess(ruta, sede)` reemplaza los 4 métodos duplicados.

## Estructura de Archivos

```
v2.0_Semana04_SRP_DRY/
└── src/
    ├── Models/
    │   ├── Empleado.cs          ← SRP: Entidad de dominio (solo datos del empleado)
    │   ├── Asistencia.cs        ← SRP: Entidad de dominio (solo datos de asistencia)
    │   └── Permiso.cs           ← SRP: Entidad de dominio (solo datos de permiso)
    ├── DataAccess/
    │   ├── DatabaseHelper.cs    ← DRY: Centraliza conexión y ejecución de queries
    │   ├── EmpleadoRepository.cs    ← SRP: Solo operaciones CRUD de empleados
    │   └── AsistenciaRepository.cs  ← SRP: Solo operaciones de asistencia
    └── Services/
        └── AsistenciaImportService.cs  ← SRP + DRY: Importación parametrizada
```

## Métricas de Mejora

| Métrica | Antes (v1.0) | Después (v2.0) |
|---------|:------------:|:--------------:|
| Clases con responsabilidad única | 0 | 6 |
| Bloques de conexión duplicados | 15+ | 1 (centralizado) |
| Métodos de importación duplicados | 4 | 1 (parametrizado) |
| Líneas de código duplicadas eliminadas | — | ~210 líneas |

## Relación con v1.0
Los comentarios `// ANTES:` en cada archivo referencian exactamente qué parte de `ClassRRHH_Original.vb` se refactorizó y por qué.
