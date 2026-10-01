// v3.0 - Acumulativo desde v2.0 | DataAccess/EmpleadoRepository.cs | SRP + DRY
using System; using System.Data; using System.Data.SqlClient; using RRHH.Models;

namespace RRHH.DataAccess
{
    public class EmpleadoRepository
    {
        private readonly DatabaseHelper _db;
        public EmpleadoRepository(DatabaseHelper db) { _db = db; }

        public DataTable ObtenerTodos() => _db.ExecuteQuery("spRRHH_ListarTrabajadores");

        public DataTable BuscarPorCodigo(string codigoEmpleado) =>
            _db.ExecuteQuery("spRRHH_ListarTrabajadores", new SqlParameter("@CodigoEmpleado", codigoEmpleado));

        public DataTable BuscarPersonas(string criterio) =>
            _db.ExecuteQuery("spRRHH_BuscarPersonas", new SqlParameter("@criterio", criterio));

        public void Insertar(Empleado empleado) =>
            _db.ExecuteNonQuery("spRRHH_Ingresa_Empleado",
                new SqlParameter("@idEmpleado", empleado.IdEmpleado),
                new SqlParameter("@codigo", empleado.CodigoEmpleado),
                new SqlParameter("@idPersona", empleado.IdPersona),
                new SqlParameter("@idCargo", empleado.IdCargo),
                new SqlParameter("@idArea", empleado.IdArea),
                new SqlParameter("@fechaIngreso", empleado.FechaIngreso));

        public void Actualizar(Empleado empleado) =>
            _db.ExecuteNonQuery("spRRHH_Actualiza_Empleado",
                new SqlParameter("@idEmpleado", empleado.IdEmpleado),
                new SqlParameter("@codigo", empleado.CodigoEmpleado),
                new SqlParameter("@idCargo", empleado.IdCargo),
                new SqlParameter("@idArea", empleado.IdArea));

        public void ActualizarArea(int idEmpleado, int idArea) =>
            _db.ExecuteNonQuery("spRRHH_Actualizar_Area",
                new SqlParameter("@idEmpleado", idEmpleado),
                new SqlParameter("@idArea", idArea));
    }
}
