// ============================================================================
// v3.0 - REFACTORIZACIÓN SEMANA 5: Principio Abierto-Cerrado (OCP)
// Archivo: Interfaces/IAsistenciaImporter.cs
// ANTES (v2.0): AsistenciaImportService tenía un solo método ImportarDesdeAccess
//        que estaba parametrizado (corregía DRY), pero si mañana se necesita
//        importar desde CSV, Excel, API REST o cualquier otra fuente,
//        habría que MODIFICAR la clase existente → viola OCP.
// AHORA: Definimos una INTERFAZ (abstracción) que permite EXTENDER el sistema
//        con nuevos importadores SIN MODIFICAR el código existente.
//        OCP: Abierto a extensión (nuevas clases), cerrado a modificación.
// ============================================================================

namespace RRHH.Interfaces
{
    /// <summary>
    /// Abstracción para importadores de asistencias.
    /// OCP: Cualquier nueva fuente de datos (CSV, Excel, API, etc.)
    /// se implementa como una nueva clase que hereda esta interfaz,
    /// SIN necesidad de modificar el código existente.
    /// </summary>
    public interface IAsistenciaImporter
    {
        /// <summary>
        /// Nombre descriptivo del importador.
        /// </summary>
        string Nombre { get; }

        /// <summary>
        /// Importa asistencias desde la fuente de datos configurada.
        /// </summary>
        /// <param name="sede">Nombre de la sede a importar</param>
        /// <returns>Cantidad de registros importados</returns>
        int Importar(string sede);

        /// <summary>
        /// Verifica si el importador puede manejar la fuente de datos.
        /// </summary>
        bool PuedeImportar(string rutaOrigen);
    }
}
