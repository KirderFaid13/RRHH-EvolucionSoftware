using System;
using System.Data.SqlClient;

namespace ClassRRHH;

// Mantiene juntos el comando y el nombre usado por Fill(DataSet, nombreTabla).
public sealed class ComandoReporte : IDisposable
{
    public SqlCommand Comando { get; }
    public string NombreTabla { get; }

    internal ComandoReporte(SqlCommand comando, string nombreTabla)
    {
        Comando = comando;
        NombreTabla = nombreTabla;
    }

    public void Dispose()
    {
        Comando.Dispose();
    }
}
