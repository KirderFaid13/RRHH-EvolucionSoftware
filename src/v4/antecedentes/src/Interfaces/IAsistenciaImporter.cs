// v4.0 - Acumulativo | Interfaces/IAsistenciaImporter.cs (desde v3.0)
namespace RRHH.Interfaces
{
    public interface IAsistenciaImporter
    {
        string Nombre { get; }
        int Importar(string sede);
        bool PuedeImportar(string rutaOrigen);
    }
}
