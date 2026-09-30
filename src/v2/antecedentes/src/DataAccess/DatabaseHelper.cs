// ============================================================================
// v2.0 - REFACTORIZACIÓN SEMANA 4: Principio SRP + DRY
// Archivo: DataAccess/DatabaseHelper.cs
// ANTES: La conexión a BD se repetía en CADA método de ClassRRHH.vb:
//        "Dim cn As New SqlConnection(Conexion)" aparecía +15 veces.
//        Cada método abría y cerraba la conexión manualmente sin manejo
//        de errores ni reutilización.
// AHORA: Clase utilitaria que centraliza el acceso a BD.
//        Aplica DRY: la lógica de conexión se escribe UNA SOLA VEZ.
//        Aplica SRP: solo se encarga de gestionar conexiones SQL.
// ============================================================================

using System;
using System.Data;
using System.Data.SqlClient;

namespace RRHH.DataAccess
{
    /// <summary>
    /// Helper centralizado para acceso a base de datos SQL Server.
    /// DRY: Elimina la duplicación de código de conexión que existía en ClassRRHH.
    /// SRP: Solo gestiona la conexión y ejecución de comandos SQL.
    /// </summary>
    public class DatabaseHelper
    {
        private readonly string _connectionString;

        public DatabaseHelper(string connectionString)
        {
            _connectionString = connectionString;
        }

        // ANTES (código repetido en cada método de ClassRRHH.vb):
        //   Dim cn As New SqlConnection(Conexion)
        //   Dim cmd As New SqlCommand("sp_nombre", cn)
        //   cmd.CommandType = CommandType.StoredProcedure
        //   cn.Open()
        //   ...
        //   cn.Close()
        //
        // AHORA: Un solo método reutilizable con manejo de errores

        /// <summary>
        /// Ejecuta un stored procedure que retorna datos (SELECT).
        /// </summary>
        public DataTable ExecuteQuery(string storedProcedure, params SqlParameter[] parameters)
        {
            using (var connection = new SqlConnection(_connectionString))
            using (var command = new SqlCommand(storedProcedure, connection))
            {
                command.CommandType = CommandType.StoredProcedure;

                if (parameters != null)
                    command.Parameters.AddRange(parameters);

                var dataTable = new DataTable();
                var adapter = new SqlDataAdapter(command);

                connection.Open();
                adapter.Fill(dataTable);
                // La conexión se cierra automáticamente con 'using'

                return dataTable;
            }
        }

        /// <summary>
        /// Ejecuta un stored procedure que no retorna datos (INSERT/UPDATE/DELETE).
        /// </summary>
        public int ExecuteNonQuery(string storedProcedure, params SqlParameter[] parameters)
        {
            using (var connection = new SqlConnection(_connectionString))
            using (var command = new SqlCommand(storedProcedure, connection))
            {
                command.CommandType = CommandType.StoredProcedure;

                if (parameters != null)
                    command.Parameters.AddRange(parameters);

                connection.Open();
                return command.ExecuteNonQuery();
            }
        }

        /// <summary>
        /// Ejecuta un stored procedure que retorna un valor escalar.
        /// </summary>
        public object ExecuteScalar(string storedProcedure, params SqlParameter[] parameters)
        {
            using (var connection = new SqlConnection(_connectionString))
            using (var command = new SqlCommand(storedProcedure, connection))
            {
                command.CommandType = CommandType.StoredProcedure;

                if (parameters != null)
                    command.Parameters.AddRange(parameters);

                connection.Open();
                return command.ExecuteScalar();
            }
        }
    }
}
