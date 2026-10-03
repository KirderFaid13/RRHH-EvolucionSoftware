// v4.0 - Acumulativo | Interfaces/IReporteGenerator.cs (desde v3.0)
using System.Data;

namespace RRHH.Interfaces
{
    public interface IReporteGenerator
    {
        string NombreReporte { get; }
        DataTable Generar(params object[] parametros);
        string Descripcion { get; }
    }
}
