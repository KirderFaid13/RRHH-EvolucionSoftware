// ============================================================================
// v2.0 - REFACTORIZACIÓN SEMANA 4: Principio SRP + DRY
// Archivo: Models/Empleado.cs
// ANTES: Los datos del empleado estaban mezclados dentro de ClassRRHH.vb
//        como propiedades sueltas (mCodigoEmpleado, etc.) sin una entidad clara.
// AHORA: Clase dedicada exclusivamente a representar la entidad Empleado.
//        Cumple SRP: solo tiene UNA responsabilidad = definir los datos del empleado.
// ============================================================================

namespace RRHH.Models
{
    /// <summary>
    /// Entidad de dominio que representa un Empleado.
    /// SRP: Solo contiene propiedades de datos, sin lógica de negocio ni acceso a BD.
    /// </summary>
    public class Empleado
    {
        public int IdEmpleado { get; set; }
        public string CodigoEmpleado { get; set; }
        public int IdPersona { get; set; }
        public string Nombres { get; set; }
        public string ApellidoPaterno { get; set; }
        public string ApellidoMaterno { get; set; }
        public string DNI { get; set; }
        public int IdCargo { get; set; }
        public int IdArea { get; set; }
        public string AreaOrganizacional { get; set; }
        public int IdHorario { get; set; }
        public DateTime FechaIngreso { get; set; }
        public DateTime? FechaEgreso { get; set; }
        public bool Activo { get; set; }
    }
}
