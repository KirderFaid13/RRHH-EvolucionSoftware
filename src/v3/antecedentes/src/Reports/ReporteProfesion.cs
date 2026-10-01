// v3.0 - OCP | Reports/ReporteProfesion.cs
using System.Data; using RRHH.Interfaces; using RRHH.DataAccess;

namespace RRHH.Reports
{
    public class ReporteProfesion : IReporteGenerator
    {
        private readonly DatabaseHelper _db;
        public string NombreReporte => "Personal por Profesión";
        public string Descripcion => "Lista el personal agrupado por profesión";
        public ReporteProfesion(DatabaseHelper db) { _db = db; }
        public DataTable Generar(params object[] parametros) => _db.ExecuteQuery("spRRHH_Rep_profesion");
    }
}
