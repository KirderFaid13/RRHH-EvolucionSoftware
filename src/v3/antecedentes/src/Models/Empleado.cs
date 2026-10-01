using System;

namespace RRHH.Models
{
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
