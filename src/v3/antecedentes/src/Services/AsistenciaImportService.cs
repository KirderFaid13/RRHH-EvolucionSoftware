// v3.0 - Acumulativo desde v2.0 | Services/AsistenciaImportService.cs | SRP + DRY
using System; using System.Data; using System.Data.OleDb; using RRHH.DataAccess;

namespace RRHH.Services
{
    public class AsistenciaImportService
    {
        private readonly AsistenciaRepository _asistenciaRepo;
        public AsistenciaImportService(AsistenciaRepository asistenciaRepo) { _asistenciaRepo = asistenciaRepo; }

        public int ImportarDesdeAccess(string rutaAccess, string nombreSede)
        {
            var dtAccess = LeerDatosAccess(rutaAccess);
            int registrosImportados = 0;
            foreach (DataRow row in dtAccess.Rows)
            {
                _asistenciaRepo.InsertarMarcacion(
                    row["CodigoEmpleado"].ToString(),
                    Convert.ToDateTime(row["Fecha"]),
                    TimeSpan.Parse(row["Hora"].ToString()),
                    nombreSede);
                registrosImportados++;
            }
            return registrosImportados;
        }

        private DataTable LeerDatosAccess(string rutaAccess)
        {
            string connectionString = $"Provider=Microsoft.Jet.OLEDB.4.0;Data Source={rutaAccess}";
            using (var oleConn = new OleDbConnection(connectionString))
            using (var oleCmd = new OleDbCommand("SELECT * FROM Marcaciones", oleConn))
            {
                var adapter = new OleDbDataAdapter(oleCmd);
                var dt = new DataTable();
                oleConn.Open();
                adapter.Fill(dt);
                return dt;
            }
        }
    }
}
