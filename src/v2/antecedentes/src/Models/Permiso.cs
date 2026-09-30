// ============================================================================
// v2.0 - REFACTORIZACIÓN SEMANA 4: Principio SRP + DRY
// Archivo: Models/Permiso.cs
// ANTES: Los datos de permiso se manejaban como parámetros sueltos
//        en los métodos ExistePermiso(), ElimnarPermiso() de ClassRRHH.vb
// AHORA: Entidad propia con una sola responsabilidad.
// ============================================================================

namespace RRHH.Models
{
    /// <summary>
    /// Entidad de dominio que representa un Permiso.
    /// SRP: Solo datos del permiso.
    /// </summary>
    public class Permiso
    {
        public int IdPermiso { get; set; }
        public int IdEmpleado { get; set; }
        public DateTime FechaPermiso { get; set; }
        public string TipoPermiso { get; set; }
        public string MotivoPermiso { get; set; }
        public TimeSpan? HoraSalida { get; set; }
        public TimeSpan? HoraRetorno { get; set; }
        public string Observaciones { get; set; }
        public bool Aprobado { get; set; }
    }
}
