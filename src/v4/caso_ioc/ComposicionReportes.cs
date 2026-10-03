using System.Data.SqlClient;

namespace ClassRRHH;

// La selección y creación de la implementación queda fuera del generador.
public static class ComposicionReportes
{
    public static GeneradorReportes CrearSql(SqlConnection conexion, SqlDataAdapter adaptador)
    {
        var sql = new EjecutorReportesSql(conexion, adaptador);
        return new GeneradorReportes(conexion, sql);
    }
}
