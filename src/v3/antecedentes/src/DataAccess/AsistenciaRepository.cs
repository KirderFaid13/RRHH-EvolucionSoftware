// v3.0 - Acumulativo desde v2.0 | DataAccess/AsistenciaRepository.cs | SRP + DRY
using System; using System.Data; using System.Data.SqlClient;

namespace RRHH.DataAccess
{
    public class AsistenciaRepository
    {
        private readonly DatabaseHelper _db;
        public AsistenciaRepository(DatabaseHelper db) { _db = db; }

        public DataTable ObtenerPorDia(DateTime fecha) =>
            _db.ExecuteQuery("spRRHH_GetAsistenciaDia", new SqlParameter("@fecha", fecha));

        public void Actualizar(int idEmpleado, DateTime fecha) =>
            _db.ExecuteNonQuery("spRRHH_ActualizaAsistencia",
                new SqlParameter("@idEmpleado", idEmpleado), new SqlParameter("@fecha", fecha));

        public bool Existe(int idEmpleado, DateTime fecha) =>
            Convert.ToBoolean(_db.ExecuteScalar("spRRHH_ExisteAsistencia",
                new SqlParameter("@idEmpleado", idEmpleado), new SqlParameter("@fecha", fecha)));

        public void LlenarPlanilla(string anio, string mes) =>
            _db.ExecuteNonQuery("spRRHH_LlenarPlanillaAsistencia",
                new SqlParameter("@anio", anio), new SqlParameter("@mes", mes));

        public void InsertarMarcacion(string codigoEmpleado, DateTime fecha, TimeSpan hora, string sede) =>
            _db.ExecuteNonQuery("spRRHH_InsertarMarcacion",
                new SqlParameter("@codempleado", codigoEmpleado), new SqlParameter("@fecha", fecha),
                new SqlParameter("@hora", hora), new SqlParameter("@sede", sede));
    }
}
