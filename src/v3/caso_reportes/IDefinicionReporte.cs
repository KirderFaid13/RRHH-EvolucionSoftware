using System.Data.SqlClient;

namespace ClassRRHH;

// C04: punto de extensión para los contratos de reporte, no para acceso a SQL.
public interface IDefinicionReporte
{
    string NombreTabla { get; }
    SqlCommand CrearComando(SqlConnection conexion);
}
