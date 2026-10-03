// v4.0 - DIP | Interfaces/IPermisoRepository.cs
using System; using System.Data; using RRHH.Models;

namespace RRHH.Interfaces
{
    public interface IPermisoRepository
    {
        bool Existe(int idEmpleado, DateTime fecha);
        void Eliminar(int idPermiso);
        int ObtenerSiguienteId();
        void Registrar(Permiso permiso);
        DataTable ListarPorEmpleado(int idEmpleado);
    }
}
