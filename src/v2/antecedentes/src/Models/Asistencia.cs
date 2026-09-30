// ============================================================================
// v2.0 - REFACTORIZACIÓN SEMANA 4: Principio SRP + DRY
// Archivo: Models/Asistencia.cs
// ANTES: No existía como entidad independiente. Los datos de asistencia
//        se manejaban directamente como DataRows dentro de ClassRRHH.vb.
// AHORA: Clase independiente con responsabilidad única de representar
//        los datos de una asistencia.
// ============================================================================

namespace RRHH.Models
{
    /// <summary>
    /// Entidad de dominio que representa un registro de Asistencia.
    /// SRP: Solo datos, sin lógica de importación ni validación.
    /// </summary>
    public class Asistencia
    {
        public int IdAsistencia { get; set; }
        public int IdEmpleado { get; set; }
        public string CodigoEmpleado { get; set; }
        public DateTime Fecha { get; set; }
        public TimeSpan? HoraEntrada { get; set; }
        public TimeSpan? HoraSalida { get; set; }
        public string Sede { get; set; }
        public string Estado { get; set; } // Presente, Falta, Tardanza, Permiso
        public bool EsManual { get; set; }
    }
}
