// ============================================================================
// v2.0 - REFACTORIZACIÓN SEMANA 4: Principio SRP + DRY
// Archivo: DataAccess/AsistenciaRepository.cs
// ANTES: Los métodos de asistencia estaban dentro de ClassRRHH.vb junto
//        con empleados, permisos y reportes (violación SRP).
// AHORA: Repositorio con responsabilidad única = acceso a datos de asistencias.
// ============================================================================

using System;
using System.Data;
using System.Data.SqlClient;

namespace RRHH.DataAccess
{
    /// <summary>
    /// Repositorio exclusivo para operaciones de Asistencia en SQL Server.
    /// SRP: Solo acceso a datos de asistencias.
    /// DRY: Usa DatabaseHelper, elimina la repetición de conexiones.
    /// </summary>
    public class AsistenciaRepository
    {
        private readonly DatabaseHelper _db;

        public AsistenciaRepository(DatabaseHelper db)
        {
            _db = db;
        }

        public DataTable ObtenerPorDia(DateTime fecha)
        {
            return _db.ExecuteQuery("spRRHH_GetAsistenciaDia",
                new SqlParameter("@fecha", fecha));
        }

        public void Actualizar(int idEmpleado, DateTime fecha)
        {
            _db.ExecuteNonQuery("spRRHH_ActualizaAsistencia",
                new SqlParameter("@idEmpleado", idEmpleado),
                new SqlParameter("@fecha", fecha));
        }

        public bool Existe(int idEmpleado, DateTime fecha)
        {
            var result = _db.ExecuteScalar("spRRHH_ExisteAsistencia",
                new SqlParameter("@idEmpleado", idEmpleado),
                new SqlParameter("@fecha", fecha));
            return Convert.ToBoolean(result);
        }

        public void LlenarPlanilla(string anio, string mes)
        {
            _db.ExecuteNonQuery("spRRHH_LlenarPlanillaAsistencia",
                new SqlParameter("@anio", anio),
                new SqlParameter("@mes", mes));
        }

        public void InsertarMarcacion(string codigoEmpleado, DateTime fecha,
                                       TimeSpan hora, string sede)
        {
            _db.ExecuteNonQuery("spRRHH_InsertarMarcacion",
                new SqlParameter("@codempleado", codigoEmpleado),
                new SqlParameter("@fecha", fecha),
                new SqlParameter("@hora", hora),
                new SqlParameter("@sede", sede));
        }
    }
}
