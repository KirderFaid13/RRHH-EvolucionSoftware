using System.Data;
using System.Data.SqlClient;

namespace ClassRRHH;

public sealed class GeneradorReportes
{
    private readonly SqlConnection _conexion;
    private readonly EjecutorReportesSql _sql;

    public GeneradorReportes(SqlConnection conexion, SqlDataAdapter adaptador)
    {
        _conexion = conexion;
        _sql = new EjecutorReportesSql(conexion, adaptador);
    }

    public ComandoReporte Preparar(IDefinicionReporte reporte)
    {
        return new ComandoReporte(reporte.CrearComando(_conexion), reporte.NombreTabla);
    }

    public DataSet Generar(IDefinicionReporte reporte)
    {
        return _sql.Ejecutar(Preparar(reporte));
    }
}
