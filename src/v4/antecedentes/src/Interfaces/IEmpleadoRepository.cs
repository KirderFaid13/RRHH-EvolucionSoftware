// v4.0 - DIP | Interfaces/IEmpleadoRepository.cs
using System.Data; using RRHH.Models;

namespace RRHH.Interfaces
{
    public interface IEmpleadoRepository
    {
        DataTable ObtenerTodos();
        DataTable BuscarPorCodigo(string codigoEmpleado);
        DataTable BuscarPersonas(string criterio);
        void Insertar(Empleado empleado);
        void Actualizar(Empleado empleado);
        void ActualizarArea(int idEmpleado, int idArea);
    }
}
