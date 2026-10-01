using System;

namespace RRHH.Models
{
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
