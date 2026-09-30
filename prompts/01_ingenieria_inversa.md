# C02: ingeniería inversa del RRHH original

Utiliza este prompt cuando el equipo autorice avanzar al segundo commit. No ejecutarlo como parte de la preparación del primer commit.

```text
Actúa como responsable de ingeniería inversa de un sistema existente de Recursos Humanos.

Lee primero README.md, .context/01_business_rules.md,
.context/02_data_dictionary.json, .context/03_course_context.md y
.context/ROADMAP.md. Trabaja exclusivamente en la etapa C02.

Objetivo:
Recuperar y documentar conocimiento verificable del RRHH original para
preparar una base de trabajo v1. No aplicar todavía SRP/DRY, OCP ni IoC.

Trabajo:
1. Localiza la entrega original indicada por el README e inventaría sus
   archivos. Distingue fuentes, binarios, configuración, documentación,
   datos y dependencias sin alterar sus originales.
2. Identifica tecnologías, módulos, puntos de entrada, dependencias y
   rutas de acceso a datos a partir de evidencias citables.
3. Lee la documentación disponible y contrasta sus afirmaciones con
   los artefactos técnicos. Registra cualquier discrepancia.
4. Si hay código fuente original, conserva su procedencia. Si solo hay
   binarios y necesitas descompilar, documenta el archivo de origen,
   la herramienta y el procedimiento utilizado. Distingue claramente
   la descompilación de una reconstrucción o propuesta manual.
5. Registra las reglas funcionales y el modelo de datos que realmente
   puedas recuperar. No inventes roles, campos, tablas, relaciones,
   firmas de procedimientos ni funciones para completar huecos.
6. Define la v1 según lo que efectivamente se haya recuperado. Si es
   parcial o no ejecutable, indícalo y registra qué falta. Mantén el
   código recuperado separado de la entrega original.
7. Realiza las comprobaciones pertinentes que permita el entorno.
   Conserva comandos y resultados. Diferencia análisis estático,
   compilación y ejecución; una compilación no demuestra la operación
   real del sistema ni de su base de datos.
8. Actualiza el contexto solo con hallazgos sustentados y prepara la
   documentación descriptiva del segundo commit.

Límites:
- No publiques credenciales ni datos personales en archivos, informes
  o mensajes de commit. Usa ejemplos sin valores reales.
- No ejecutes binarios ni restaures datos para suplir información
  desconocida sin evaluar primero la operación concreta y su alcance.
- No presentes toda creación de objetos como un defecto: identifica
  qué dependencia existe y qué efecto puede demostrar la evidencia.
- No cambies el comportamiento del RRHH como parte de esta etapa.
- No avances a C03 hasta que el equipo lo indique.

Entrega:
Documentación ordenada de la ingeniería inversa, código recuperado
con procedencia explícita si lo hay, evidencias de las comprobaciones,
lista de límites pendientes y mensaje de commit que explique qué se
incorporó y por qué sirve como base de las refactorizaciones.

Al finalizar, explica al equipo qué hiciste, dónde está, por qué lo
hiciste y qué conocimiento recuperaste. Tras el segundo commit,
detén el trabajo y espera la indicación para continuar.
```
