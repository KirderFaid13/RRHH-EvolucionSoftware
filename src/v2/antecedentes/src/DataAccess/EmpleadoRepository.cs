// ============================================================================
// v2.0 - REFACTORIZACIÓN SEMANA 4: Principio SRP + DRY
// Archivo: DataAccess/EmpleadoRepository.cs
// ANTES: Los métodos ObtenerEmpleados(), BuscarEmpleado_Codigo(),
//        Ingresa_Empleado(), Actualiza_Empleado(), Actualizar_Area_Empleado()
//        y BuscarPersonas() estaban TODOS dentro de ClassRRHH.vb junto con
//        los métodos de asistencias, permisos y reportes.
// AHORA: Repositorio dedicado exclusivamente a operaciones de Empleado.
//        SRP: Solo tiene UNA responsabilidad = acceso a datos de empleados.
//        DRY: Usa DatabaseHelper en vez de repetir la conexión en cada método.
// ============================================================================

using System;
using System.Data;
using System.Data.SqlClient;
using RRHH.Models;

namespace RRHH.DataAccess
{
    /// <summary>
    /// Repositorio exclusivo para operaciones CRUD de Empleado.
    /// SRP: Solo se encarga del acceso a datos de empleados.
    /// DRY: Reutiliza DatabaseHelper para todas las operaciones.
    /// </summary>
    public class EmpleadoRepository
    {
        private readonly DatabaseHelper _db;

        public EmpleadoRepository(DatabaseHelper db)
        {
            _db = db;
        }

        // ANTES en ClassRRHH.vb (6 líneas de boilerplate por método):
        //   Dim cn As New SqlConnection(Conexion)
        //   Dim cmd As New SqlCommand("spRRHH_ListarTrabajadores", cn)
        //   cmd.CommandType = CommandType.StoredProcedure
        //   Dim da As New SqlDataAdapter(cmd)
        //   cn.Open() ... cn.Close()
        //
        // AHORA: Una sola línea gracias a DatabaseHelper (DRY)
        public DataTable ObtenerTodos()
        {
            return _db.ExecuteQuery("spRRHH_ListarTrabajadores");
        }

        public DataTable BuscarPorCodigo(string codigoEmpleado)
        {
            return _db.ExecuteQuery("spRRHH_ListarTrabajadores",
                new SqlParameter("@CodigoEmpleado", codigoEmpleado));
        }

        public DataTable BuscarPersonas(string criterio)
        {
            return _db.ExecuteQuery("spRRHH_BuscarPersonas",
                new SqlParameter("@criterio", criterio));
        }

        public void Insertar(Empleado empleado)
        {
            _db.ExecuteNonQuery("spRRHH_Ingresa_Empleado",
                new SqlParameter("@idEmpleado", empleado.IdEmpleado),
                new SqlParameter("@codigo", empleado.CodigoEmpleado),
                new SqlParameter("@idPersona", empleado.IdPersona),
                new SqlParameter("@idCargo", empleado.IdCargo),
                new SqlParameter("@idArea", empleado.IdArea),
                new SqlParameter("@fechaIngreso", empleado.FechaIngreso));
        }

        public void Actualizar(Empleado empleado)
        {
            _db.ExecuteNonQuery("spRRHH_Actualiza_Empleado",
                new SqlParameter("@idEmpleado", empleado.IdEmpleado),
                new SqlParameter("@codigo", empleado.CodigoEmpleado),
                new SqlParameter("@idCargo", empleado.IdCargo),
                new SqlParameter("@idArea", empleado.IdArea));
        }

        public void ActualizarArea(int idEmpleado, int idArea)
        {
            _db.ExecuteNonQuery("spRRHH_Actualizar_Area",
                new SqlParameter("@idEmpleado", idEmpleado),
                new SqlParameter("@idArea", idArea));
        }
    }
}
