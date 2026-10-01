// ============================================================================
// v3.0 - REFACTORIZACIÓN SEMANA 5: Principio Abierto-Cerrado (OCP)
// Archivo: Importers/AccessImporter.cs
// Implementación concreta de IAsistenciaImporter para archivos Access (.mdb)
// Esta es la versión OCP del AsistenciaImportService de la v2.0.
// OCP: Si mañana se necesita importar desde otra fuente, se crea una NUEVA
//      clase (ej: CsvImporter, ExcelImporter) sin tocar esta.
// ============================================================================

using System;
using System.Data;
using System.Data.OleDb;
using RRHH.Interfaces;
using RRHH.DataAccess;

namespace RRHH.Importers
{
    /// <summary>
    /// Importador de asistencias desde bases de datos Microsoft Access.
    /// OCP: Implementación concreta para Access. Nuevas fuentes = nuevas clases.
    /// </summary>
    public class AccessImporter : IAsistenciaImporter
    {
        private readonly AsistenciaRepository _repo;
        private readonly string _rutaAccess;

        public string Nombre => "Importador Access (.mdb)";

        public AccessImporter(AsistenciaRepository repo, string rutaAccess)
        {
            _repo = repo;
            _rutaAccess = rutaAccess;
        }

        public bool PuedeImportar(string rutaOrigen)
        {
            return rutaOrigen.EndsWith(".mdb", StringComparison.OrdinalIgnoreCase)
                || rutaOrigen.EndsWith(".accdb", StringComparison.OrdinalIgnoreCase);
        }

        public int Importar(string sede)
        {
            var dtAccess = LeerDatosAccess();
            int registros = 0;

            foreach (DataRow row in dtAccess.Rows)
            {
                _repo.InsertarMarcacion(
                    row["CodigoEmpleado"].ToString(),
                    Convert.ToDateTime(row["Fecha"]),
                    TimeSpan.Parse(row["Hora"].ToString()),
                    sede);
                registros++;
            }
            return registros;
        }

        private DataTable LeerDatosAccess()
        {
            string connStr = $"Provider=Microsoft.Jet.OLEDB.4.0;Data Source={_rutaAccess}";
            using (var conn = new OleDbConnection(connStr))
            using (var cmd = new OleDbCommand("SELECT * FROM Marcaciones", conn))
            {
                var dt = new DataTable();
                var adapter = new OleDbDataAdapter(cmd);
                conn.Open();
                adapter.Fill(dt);
                return dt;
            }
        }
    }
}
