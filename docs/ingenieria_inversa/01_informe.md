# C02: ingeniería inversa del RRHH y base v1

Documentación del 30 de septiembre de 2026, Lima. Esta etapa recupera conocimiento y código del legado para fundamentar sus refactorizaciones. El ejecutable y los archivos del primer commit conservan su contenido.

## Qué se hizo y por qué

Se inspeccionó estáticamente la distribución, se recuperó código del ensamblado propio `ClassRRHH.dll` con ILSpyCMD y se contrastó el antecedente académico v1 con esa evidencia. El resultado permite elegir un caso sobre clases, firmas y consultas reales, evitando atribuir al sistema una arquitectura que solo existía en el ejemplo previo.

| Trabajo | Ubicación | Aporte |
| --- | --- | --- |
| Inventario técnico y metadatos | [evidencia](../../evidencia/ingenieria_inversa/README.md) | Identificar plataforma, dependencias y tipos sin ejecutar la aplicación. |
| Recuperación de código | [src/v1](../../src/v1/README.md) | Inspeccionar cuerpos y llamadas reales del ensamblado de negocio. |
| Arquitectura recuperada | [diagrama y explicación](02_arquitectura.md) | Ubicar responsabilidades y dependencias antes de proponer un cambio. |
| Procedencia y compilación | [procedimiento](03_procedencia_v1.md) | Relacionar cada fuente con el binario y distinguir compilación de funcionamiento. |
| Auditoría del trabajo previo | [antecedente v1](04_revision_antecedente.md) | Conservar y corregir la descripción de la reconstrucción anterior. |
| Memoria actualizada | [reglas](../../.context/01_business_rules.md) y [diccionario](../../.context/02_data_dictionary.json) | Dar contexto verificable a las siguientes tareas y mantener visibles los desconocidos. |

## Hallazgos técnicos

La distribución restaurada comprende 347 archivos; el BAK permanece local. Los 250 PE —244 DLL y seis EXE— contienen metadatos CLR `v2.0.50727`. Las referencias a bibliotecas 2.0 y 3.5 corresponden a la familia .NET Framework de esa época; el número de CLR no determina por sí solo un framework objetivo. El ejecutable principal y `ClassRRHH.dll` requieren 32 bits. Hay Windows Forms, referencias Microsoft.VisualBasic y DevExpress 11.2.7; otras versiones de DevExpress también están presentes en el paquete.

El ejecutable principal contiene 216 definiciones de tipos, 9.509 métodos y 89 recursos. Esos recuentos incluyen formularios y código generado; no miden exclusivamente lógica de negocio. Se observaron `MainMDI` y métodos de `BackgroundWorker` en cinco formularios de importación; esto no demuestra por sí solo qué ocurre durante su ejecución.

La DLL separa cuatro clases de negocio: `RRHHClass`, `AsistenciaAccess`, `FamiliaresClass` y `FichaSocialClass`. Se recuperaron sus cuerpos y ocho fuentes de soporte, para un total de 12 archivos C#. El C# es salida del descompilador; no son los archivos VB originales ni una nueva implementación.

## Contratos recuperados relevantes

| Operación del cliente | Contrato observado | Fuente |
| --- | --- | --- |
| Importación Access → SQL | Cuatro `Access2Sql*` en `AsistenciaAccess`, con `FechaInicial`, `FechaFinal` y `forzar`. Consultan `empleado`, `asis_norm` y `marcacion` y generan texto `EXEC` para dos procedimientos. | [AsistenciaAccess.cs](../../src/v1/recuperado/ClassRRHH/AsistenciaAccess.cs). |
| Reporte por código de oficina | `Generar_Report_oficina(int CodOficina)` llama `spRRHH_Report_Oficina_Unico`, parámetro `@idarea` de tipo `SqlDbType.Int`. | [RRHHClass.cs](../../src/v1/recuperado/ClassRRHH/RRHHClass.cs), líneas 664–674. |
| Reporte por sigla | `Generar_Report_oficina_Dep(string Sigla)` llama `spRRHH_Report_Oficina`, parámetro `@sigla` de tipo `VarChar`. | Mismo archivo, líneas 676–686. |
| Familiares de ficha | `llenarFamiliares(int CodEmple)` llama `spRRHH_BuscarFamiliares` con `@idempleado`, tipo `Int`. | [FichaSocialClass.cs](../../src/v1/recuperado/ClassRRHH/FichaSocialClass.cs). |

En particular, el nombre `spRRHH_Report_Oficina` no justifica asumir un argumento entero `@idOficina`. Los dos métodos recuperados distinguen consultas y parámetros. Antes de implementar una mejora, se debe elegir cuál se pretende conservar y verificar su contrato real cuando se disponga de CMI.

El código muestra SQL concatenado, administración manual de conexiones y repetición entre importadores. Se registran como candidatos de mantenimiento. Su corrección y cualquier separación de responsabilidades se realizarán en una etapa posterior, con un alcance explícito.

## Distribución y documentación

Los 84 XML/configuraciones/manifiestos son bien formados. En los tres manifiestos principales aparecen 84, 12 y tres referencias ausentes según la carpeta. Al revisar los 12 manifiestos de aplicación y ejecutable hay 270 ocurrencias de referencias ausentes, cuatro diferencias de tamaño y 12 de digest; las ocurrencias incluyen declaraciones repetidas y no representan 270 archivos distintos. No se verificó instalación ClickOnce.

Los 348 originales tienen 239 contenidos distintos y 68 grupos de duplicados, con 115.345.957 bytes redundantes dentro de este paquete. Las copias se conservan: compartir nombre no acredita identidad y este commit no limpia dependencias.

La revisión de ocho PDF, 119 páginas, relaciona la recuperación con el sílabo y la guía final. [Páginas y conclusiones del curso](04_revision_antecedente.md). No se encontró una consigna independiente de semana 03 entre estos documentos.

## Comprobaciones y límites

Las 12 fuentes recuperadas compilaron como biblioteca x86 usando Roslyn del SDK 10.0.103 y referencias Framework instaladas en `v4.0.30319`: cero errores y advertencias. Se cotejaron firmas y campos públicos de las cuatro clases contra el original mediante IL estático. También se verificaron hashes de fuentes, conservación del baseline, enlaces, JSON y exclusiones de material privado.

La compilación usa referencias del entorno y no valida el framework original inferido como `net35`, recursos, firma, interfaz ni despliegue. No se ejecutó RRHH, no se conectó SQL/Access y no se restauró CMI. La existencia y firma efectiva de los procedimientos, las restricciones de datos, permisos por actor y equivalencia funcional siguen pendientes.

El cierre de C02 entrega una **base de ingeniería inversa parcial y verificable**. No constituye recuperación completa de la aplicación ni refactorización SRP/DRY, OCP o IoC. Se detiene después del segundo commit; C03 requiere la indicación del equipo.
