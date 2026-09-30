using System.Data;
using System.Data.SqlClient;

namespace ClassRRHH;

// C03: consultas de empleados. Contratos tomados de RRHHClass recuperada.
public sealed class EmpleadoConsultas
{
    private readonly EjecutorConsultasSql _sql;

    public EmpleadoConsultas(SqlConnection conexion, SqlDataAdapter adaptador)
    {
        _sql = new EjecutorConsultasSql(conexion, adaptador);
    }

    public DataTable ObtenerEmpleados()
    {
        return _sql.EjecutarConsulta(CrearComandoObtenerEmpleados(), true);
    }

    public DataTable BuscarEmpleado_Codigo(int codigo)
    {
        return _sql.EjecutarConsulta(CrearComandoBuscarEmpleado(codigo), false);
    }

    public DataTable spRRHH_ListarTrabajadores(int idTipoTrabajador)
    {
        return _sql.EjecutarConsulta(CrearComandoListarTrabajadores(idTipoTrabajador), true);
    }

    internal SqlCommand CrearComandoObtenerEmpleados()
    {
        return _sql.CrearComando("select idempleado,NombresC from vs_GetEmpleado where Estado=1", CommandType.Text);
    }

    internal SqlCommand CrearComandoBuscarEmpleado(int codigo)
    {
        return _sql.CrearComando("spRRHH_BuscarEmpleado_Codigo", CommandType.StoredProcedure,
            new SqlParameter("@codigo", SqlDbType.Int) { Value = codigo });
    }

    internal SqlCommand CrearComandoListarTrabajadores(int idTipoTrabajador)
    {
        return _sql.CrearComando("spRRHH_ListarTrabajadores", CommandType.StoredProcedure,
            new SqlParameter("@IdTipoTrabajador", SqlDbType.Int) { Value = idTipoTrabajador });
    }
}
