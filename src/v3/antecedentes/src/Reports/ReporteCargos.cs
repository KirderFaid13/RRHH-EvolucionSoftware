// v3.0 - OCP | Reports/ReporteCargos.cs
using System.Data; using RRHH.Interfaces; using RRHH.DataAccess;

namespace RRHH.Reports
{
    public class ReporteCargos : IReporteGenerator
    {
        private readonly DatabaseHelper _db;
        public string NombreReporte => "Personal por Cargo";
        public string Descripcion => "Lista el personal agrupado por cargo";
        public ReporteCargos(DatabaseHelper db) { _db = db; }
        public DataTable Generar(params object[] parametros) => _db.ExecuteQuery("spRRHH_Rep_cargos");
    }
}
