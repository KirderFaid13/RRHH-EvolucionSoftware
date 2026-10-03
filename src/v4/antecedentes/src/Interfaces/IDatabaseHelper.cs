// v4.0 - DIP | Interfaces/IDatabaseHelper.cs
// ANTES: DatabaseHelper era concreto. Todos dependían de él directamente.
// AHORA: Interfaz que permite sustituir SQL Server por MySQL, SQLite, Mock, etc.
using System.Data; using System.Data.SqlClient;

namespace RRHH.Interfaces
{
    public interface IDatabaseHelper
    {
        DataTable ExecuteQuery(string storedProcedure, params SqlParameter[] parameters);
        int ExecuteNonQuery(string storedProcedure, params SqlParameter[] parameters);
        object ExecuteScalar(string storedProcedure, params SqlParameter[] parameters);
    }
}
