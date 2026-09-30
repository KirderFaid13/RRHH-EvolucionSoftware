using System.Data;
using System.Data.SqlClient;

namespace ClassRRHH;

// C03: mecanica ADO.NET compartida. Conserva conexion/adaptador del legado.
public sealed class EjecutorConsultasSql
{
    private readonly SqlConnection _conexion;
    private readonly SqlDataAdapter _adaptador;

    public EjecutorConsultasSql(SqlConnection conexion, SqlDataAdapter adaptador)
    {
        _conexion = conexion;
        _adaptador = adaptador;
    }

    internal SqlCommand CrearComando(string texto, CommandType tipo, params SqlParameter[] parametros)
    {
        var comando = new SqlCommand(texto, _conexion) { CommandType = tipo };
        if (parametros != null)
            comando.Parameters.AddRange(parametros);
        return comando;
    }

    public DataTable EjecutarConsulta(SqlCommand comando, bool aperturaCondicional)
    {
        if (!aperturaCondicional || _conexion.State == ConnectionState.Closed)
            _conexion.Open();
        var resultado = new DataTable();
        _adaptador.SelectCommand = comando;
        _adaptador.Fill(resultado);
        if (!aperturaCondicional || _conexion.State == ConnectionState.Open)
            _conexion.Close();
        return resultado;
    }
}
