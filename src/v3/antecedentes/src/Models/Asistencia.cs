using System;

namespace RRHH.Models
{
    public class Asistencia
    {
        public int IdAsistencia { get; set; }
        public int IdEmpleado { get; set; }
        public string CodigoEmpleado { get; set; }
        public DateTime Fecha { get; set; }
        public TimeSpan? HoraEntrada { get; set; }
        public TimeSpan? HoraSalida { get; set; }
        public string Sede { get; set; }
        public string Estado { get; set; }
        public bool EsManual { get; set; }
    }
}
