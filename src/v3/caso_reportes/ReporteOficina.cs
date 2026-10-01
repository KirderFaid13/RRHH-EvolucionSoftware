using System.Data;
using System.Data.SqlClient;

namespace ClassRRHH;

public sealed class ReporteOficina : IDefinicionReporte
{
    private readonly int _codOficina;

    public ReporteOficina(int codOficina)
    {
        _codOficina = codOficina;
    }

    public string NombreTabla => "spRRHH_Report_Oficina_Unico";

    public SqlCommand CrearComando(SqlConnection conexion)
    {
        var comando = new SqlCommand("spRRHH_Report_Oficina_Unico", conexion);
        comando.CommandType = CommandType.StoredProcedure;
        comando.Parameters.Add("@idarea", SqlDbType.Int).Value = _codOficina;
        return comando;
    }
}
