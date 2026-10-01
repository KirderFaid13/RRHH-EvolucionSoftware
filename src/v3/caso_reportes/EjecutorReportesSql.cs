using System.Data;
using System.Data.SqlClient;

namespace ClassRRHH;

// Dependencia concreta conservada. La entrega IoC queda para semana 07.
public sealed class EjecutorReportesSql
{
    private readonly SqlConnection _conexion;
    private readonly SqlDataAdapter _adaptador;

    public EjecutorReportesSql(SqlConnection conexion, SqlDataAdapter adaptador)
    {
        _conexion = conexion;
        _adaptador = adaptador;
    }

    public DataSet Ejecutar(ComandoReporte reporte)
    {
        _conexion.Open();
        var resultado = new DataSet();
        _adaptador.SelectCommand = reporte.Comando;
        _adaptador.Fill(resultado, reporte.NombreTabla);
        _conexion.Close();
        return resultado;
    }
}
