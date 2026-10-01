// v3.0 - OCP | Reports/ReporteOficina.cs
using System.Data; using System.Data.SqlClient; using RRHH.Interfaces; using RRHH.DataAccess;

namespace RRHH.Reports
{
    public class ReporteOficina : IReporteGenerator
    {
        private readonly DatabaseHelper _db;
        public string NombreReporte => "Personal por Oficina";
        public string Descripcion => "Lista el personal agrupado por oficina/área organizacional";
        public ReporteOficina(DatabaseHelper db) { _db = db; }
        public DataTable Generar(params object[] parametros)
        {
            int idOficina = parametros.Length > 0 ? (int)parametros[0] : 0;
            return _db.ExecuteQuery("spRRHH_Report_Oficina", new SqlParameter("@idOficina", idOficina));
        }
    }
}
