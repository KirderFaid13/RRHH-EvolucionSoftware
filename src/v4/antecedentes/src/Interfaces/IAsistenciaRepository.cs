// v4.0 - DIP | Interfaces/IAsistenciaRepository.cs
using System; using System.Data;

namespace RRHH.Interfaces
{
    public interface IAsistenciaRepository
    {
        DataTable ObtenerPorDia(DateTime fecha);
        void Actualizar(int idEmpleado, DateTime fecha);
        bool Existe(int idEmpleado, DateTime fecha);
        void LlenarPlanilla(string anio, string mes);
        void InsertarMarcacion(string codigoEmpleado, DateTime fecha, TimeSpan hora, string sede);
    }
}
