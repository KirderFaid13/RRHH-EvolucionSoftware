# Commits, ramas y publicación

Repositorio privado: [KirderFaid13/RRHH-EvolucionSoftware](https://github.com/KirderFaid13/RRHH-EvolucionSoftware).

## Decisión inicial: main

Se utilizará `main`, nombre predeterminado del repositorio existente. `master` puede cumplir la misma función; no hace falta mantener ambas ramas. Esta primera incorporación tiene cuatro etapas secuenciales sobre la misma línea de historia, sin ramas o merges adicionales.

Un **commit** guarda una revisión de los archivos y explica el cambio. Una **rama** permite trabajar en una mejora separada antes de incorporarla a la línea principal. Se puede recuperar una revisión anterior desde su commit aunque las posteriores estén en la misma rama. [Conceptos de Git, documentación oficial](https://docs.github.com/en/get-started/using-git/about-git).

## Cuatro commits, con una pausa por etapa

| Orden | Contenido | Explicación requerida |
| --- | --- | --- |
| 1 | RRHH original y estructura. | Qué se preserva, cómo se verifica y por qué se organiza y protege. |
| 2 | Ingeniería inversa y v1. | Qué conocimiento/código se recupera, de dónde procede y qué falta verificar. |
| 3 | v2 SRP/DRY. | Responsabilidades y duplicación del caso antes/después; motivo y comprobaciones. |
| 4 | v3 OCP. | Cambio que antes exigía modificar código y punto de extensión incorporado; verificaciones. |

Tras cada commit se comprueba la publicación, se explica al equipo lo realizado y se espera su indicación para continuar. No se retrofechan commits ni se incorporan fuentes futuras al primero para simular avances anteriores.

## Trabajo semanal posterior

Para semana 07 recomendamos una rama `semana-07-ioc`, creada desde `main` cuando se autorice ese trabajo. Permitirá revisar la dependencia concreta, aplicar la mejora, comprobarla y proponer su incorporación mediante un pull request. Las semanas siguientes pueden seguir el mismo patrón.

No se crean esas ramas en el primer commit. Los nombres v1, v2 y v3 identifican etapas del contenido; no requieren por sí solos una rama permanente cada uno.

## Cómo describir un commit

Título breve y cuerpo que indique:

1. Problema o necesidad concreta.
2. Archivos y comportamiento incorporados o modificados.
3. Motivo de la decisión.
4. Comprobaciones realmente realizadas y sus resultados.
5. Límites y pendientes relevantes.

En los siguientes commits, describir un antes/después del caso cuando se modifique código. En el primero, explicar la preservación y organización del punto de partida; no atribuirle mejoras funcionales.

## Datos y claves

`.local/` está ignorada y contiene la clave y los registros privados de publicación. No usar `git add -f` para incluir ese directorio. Los respaldos y configuraciones reales también están excluidos. El acceso al repositorio privado no reemplaza estas exclusiones.

Los archivos `*.aesgcm` del legado sí se versionan: son los originales cifrados cuya integridad está registrada. La clave se conserva fuera del historial y se comparte por un medio privado cuando el grupo la necesite. Consulta [restauración](../../legado/README.md).
