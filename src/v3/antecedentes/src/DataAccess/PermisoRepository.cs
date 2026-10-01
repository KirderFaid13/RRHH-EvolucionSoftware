// v3.0 - CORRECCIÓN: PermisoRepository (faltaba desde v2.0)
// ANTES: ExistePermiso(), ElimnarPermiso(), SgtIdPermiso() en ClassRRHH.vb
// AHORA: Repositorio dedicado con responsabilidad única (SRP + DRY)
using System; using System.Data; using System.Data.SqlClient; using RRHH.Models;

namespace RRHH.DataAccess
{
    public class PermisoRepository
    {
        private readonly DatabaseHelper _db;
        public PermisoRepository(DatabaseHelper db) { _db = db; }

        public bool Existe(int idEmpleado, DateTime fecha) =>
            Convert.ToBoolean(_db.ExecuteScalar("spRRHH_ExistePermiso",
                new SqlParameter("@idEmpleado", idEmpleado), new SqlParameter("@fecha", fecha)));

        public void Eliminar(int idPermiso) =>
            _db.ExecuteNonQuery("spRRHH_EliminarPermiso", new SqlParameter("@idPermiso", idPermiso));

        public int ObtenerSiguienteId() =>
            Convert.ToInt32(_db.ExecuteScalar("spRRHH_SgtIdPermiso"));

        public void Registrar(Permiso permiso) =>
            _db.ExecuteNonQuery("spRRHH_RegistrarPermiso",
                new SqlParameter("@idPermiso", permiso.IdPermiso),
                new SqlParameter("@idEmpleado", permiso.IdEmpleado),
                new SqlParameter("@fechaPermiso", permiso.FechaPermiso),
                new SqlParameter("@tipoPermiso", permiso.TipoPermiso),
                new SqlParameter("@motivoPermiso", permiso.MotivoPermiso),
                new SqlParameter("@observaciones", permiso.Observaciones ?? (object)DBNull.Value));

        public DataTable ListarPorEmpleado(int idEmpleado) =>
            _db.ExecuteQuery("spRRHH_ListarPermisos", new SqlParameter("@idEmpleado", idEmpleado));
    }
}
