using System.Data;
using System.Data.SqlClient;

namespace ClassRRHH;

// Segunda definición real: contrato de Generar_Report_oficina_Dep de v1.
public sealed class ReporteOficinaPorSigla : IDefinicionReporte
{
    private readonly string _sigla;

    public ReporteOficinaPorSigla(string sigla)
    {
        _sigla = sigla;
    }

    public string NombreTabla => "spRRHH_Report_Oficina";

    public SqlCommand CrearComando(SqlConnection conexion)
    {
        var comando = new SqlCommand("spRRHH_Report_Oficina", conexion);
        comando.CommandType = CommandType.StoredProcedure;
        comando.Parameters.Add("@sigla", SqlDbType.VarChar).Value = _sigla;
        return comando;
    }
}
