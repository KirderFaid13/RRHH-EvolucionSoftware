// ============================================================================
// v3.0 - REFACTORIZACIÓN SEMANA 5: Principio Abierto-Cerrado (OCP)
// Archivo: Interfaces/IReporteGenerator.cs
// ANTES: Los reportes se generaban con métodos específicos en ClassRRHH.vb:
//        Generar_Report_oficina(), generar_rep_cargos(), ListarProfesiones()
//        Si se quería agregar un nuevo reporte, había que MODIFICAR ClassRRHH.
// AHORA: Interfaz que permite agregar nuevos reportes como clases nuevas.
//        OCP: Abierto para extensión (nuevos tipos de reporte),
//        cerrado para modificación (no se toca el código existente).
// ============================================================================

using System.Data;

namespace RRHH.Interfaces
{
    /// <summary>
    /// Abstracción para generadores de reportes.
    /// OCP: Nuevos reportes se crean como nuevas clases que implementan
    /// esta interfaz. El sistema principal no necesita cambiar.
    /// </summary>
    public interface IReporteGenerator
    {
        /// <summary>
        /// Nombre descriptivo del reporte.
        /// </summary>
        string NombreReporte { get; }

        /// <summary>
        /// Genera el reporte y retorna los datos.
        /// </summary>
        DataTable Generar(params object[] parametros);

        /// <summary>
        /// Descripción del reporte para el menú.
        /// </summary>
        string Descripcion { get; }
    }
}
