// v3.0 - OCP | Reports/ReporteCumpleanos.cs
using System.Data; using RRHH.Interfaces; using RRHH.DataAccess;

namespace RRHH.Reports
{
    public class ReporteCumpleanos : IReporteGenerator
    {
        private readonly DatabaseHelper _db;
        public string NombreReporte => "Cumpleaños del Personal";
        public string Descripcion => "Lista próximos cumpleaños del personal";
        public ReporteCumpleanos(DatabaseHelper db) { _db = db; }
        public DataTable Generar(params object[] parametros) => _db.ExecuteQuery("spRRHH_Report_Cumple");
    }
}
