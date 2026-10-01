# v3.0 - Refactorización OCP (Semana 05)

## Descripción
Refactorización del sistema RRHH aplicando el **Principio Abierto-Cerrado (OCP)**. Se introducen interfaces, polimorfismo y el patrón Factory para lograr un diseño extensible sin necesidad de modificar código existente.

## Principio Aplicado

### OCP — Open-Closed Principle
> "Las entidades de software deben estar **abiertas para su extensión** pero **cerradas para su modificación**." — Bertrand Meyer

**Antes (v2.0):** Para agregar un nuevo tipo de importación o un nuevo reporte, había que modificar las clases existentes (`AsistenciaImportService`, `ClassRRHH`).  
**Después (v3.0):** Se definen interfaces (`IAsistenciaImporter`, `IReporteGenerator`) y cada implementación es una clase independiente. Agregar funcionalidad = crear nueva clase, sin tocar nada existente.

## Prerequisito
Esta versión **depende de los principios aplicados en v2.0** (SRP + DRY). Las clases con responsabilidad única de v2.0 fueron la base para definir las abstracciones de v3.0.

## Estructura de Archivos

```
v3.0_Semana05_OCP/
└── src/
    ├── Interfaces/
    │   ├── IAsistenciaImporter.cs   ← Abstracción para importadores (OCP)
    │   └── IReporteGenerator.cs     ← Abstracción para reportes (OCP)
    ├── Importers/
    │   ├── AccessImporter.cs        ← Implementación: importar desde Access
    │   ├── CsvImporter.cs           ← Implementación: importar desde CSV (EXTENSIÓN)
    │   └── ImporterFactory.cs       ← Factory: resuelve el importador correcto
    └── Reports/
        └── Reportes.cs              ← Implementaciones: ReporteOficina, ReporteCargos, etc.
```

## Demostración del OCP

### Sistema de Importación
```
                    ┌─────────────────────┐
                    │ IAsistenciaImporter  │  ← Interfaz (cerrada)
                    └─────────┬───────────┘
              ┌───────────────┼───────────────┐
    ┌─────────▼──────┐ ┌─────▼──────┐ ┌──────▼─────────┐
    │ AccessImporter │ │ CsvImporter│ │ ExcelImporter  │
    │ (existente)    │ │ (nuevo)    │ │ (futuro)       │
    └────────────────┘ └────────────┘ └────────────────┘
```

- `AccessImporter.cs` → Migra asistencias desde archivos Access (.mdb)
- `CsvImporter.cs` → **Extensión demostrada**: se agregó SIN modificar `AccessImporter` ni `ImporterFactory`

### Sistema de Reportes
```
    ┌─────────────────────┐
    │ IReporteGenerator   │  ← Interfaz (cerrada)
    └─────────┬───────────┘
    ┌─────────┼─────────┬──────────────┐
    ▼         ▼         ▼              ▼
  Oficina   Cargos   Profesión   Cumpleaños
```

Cada reporte es una clase independiente. Agregar un nuevo reporte no requiere tocar ninguno de los existentes.

## Métricas de Mejora

| Métrica | v2.0 (sin OCP) | v3.0 (con OCP) |
|---------|:--------------:|:--------------:|
| Interfaces definidas | 0 | 2 |
| Clases extensibles via polimorfismo | 0 | 6 |
| Esfuerzo para agregar nuevo importador | Modificar clase existente | Crear nueva clase |
| Esfuerzo para agregar nuevo reporte | Modificar ClassRRHH | Crear nueva clase |
| Riesgo de regresión al extender | Alto | Nulo |

## Patrones de Diseño Utilizados
- **Strategy Pattern:** Cada importador/reporte encapsula un algoritmo intercambiable
- **Factory Pattern:** `ImporterFactory` centraliza la creación y registro de importadores
- **Dependency Inversion:** El código principal depende de abstracciones (`IAsistenciaImporter`), no de implementaciones concretas
