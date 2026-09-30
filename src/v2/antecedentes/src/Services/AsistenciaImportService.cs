// ============================================================================
// v2.0 - REFACTORIZACIÓN SEMANA 4: Principio SRP + DRY
// Archivo: Services/AsistenciaImportService.cs
// ANTES: Existían 4 métodos DUPLICADOS en ClassRRHH.vb:
//        - Access2Sql()         → Importaba asistencias de SEDE
//        - Access2SqlCONSEJO()  → Importaba asistencias de CONSEJO
//        - Access2SqlPROIND()   → Importaba asistencias de PROIND
//        - Access2SqlSEDE()     → Importaba asistencias de NOSEDE
//        Los 4 hacían EXACTAMENTE lo mismo, solo cambiaba la ruta del 
//        archivo Access y el nombre de la sede. ~30 líneas x 4 = 120 líneas
//        de código duplicado.
// AHORA: UN SOLO método parametrizado que maneja cualquier sede.
//        DRY: De 120 líneas duplicadas a ~25 líneas reutilizables.
//        SRP: Solo se encarga de importar asistencias desde Access.
// ============================================================================

using System;
using System.Data;
using System.Data.OleDb;
using RRHH.DataAccess;

namespace RRHH.Services
{
    /// <summary>
    /// Servicio de importación de asistencias desde bases de datos Access.
    /// DRY: Reemplaza los 4 métodos duplicados (Access2Sql, Access2SqlCONSEJO,
    ///      Access2SqlPROIND, Access2SqlSEDE) con UN SOLO método parametrizado.
    /// SRP: Solo se encarga de la importación de asistencias.
    /// </summary>
    public class AsistenciaImportService
    {
        private readonly AsistenciaRepository _asistenciaRepo;

        public AsistenciaImportService(AsistenciaRepository asistenciaRepo)
        {
            _asistenciaRepo = asistenciaRepo;
        }

        // ANTES: 4 métodos casi idénticos, cada uno con su ruta hardcodeada
        // ----------------------------------------------------------------
        //   Public Sub Access2Sql()
        //       Dim oleConn As New OleDbConnection("...asistencias_sede.mdb")
        //       ...misma lógica...
        //       cmd.Parameters.AddWithValue("@sede", "SEDE")
        //   End Sub
        //
        //   Public Sub Access2SqlCONSEJO()     ' ← Código DUPLICADO
        //       Dim oleConn As New OleDbConnection("...asistencias_consejo.mdb")
        //       ...misma lógica...
        //       cmd.Parameters.AddWithValue("@sede", "CONSEJO")
        //   End Sub
        //   ... (2 más iguales)
        //
        // AHORA: Un solo método parametrizado (DRY)
        // ----------------------------------------------------------------

        /// <summary>
        /// Importa asistencias desde un archivo Access hacia SQL Server.
        /// Reemplaza los 4 métodos duplicados del sistema original.
        /// </summary>
        /// <param name="rutaAccess">Ruta al archivo .mdb de Access</param>
        /// <param name="nombreSede">Nombre de la sede (SEDE, CONSEJO, PROIND, NOSEDE)</param>
        /// <returns>Cantidad de registros importados</returns>
        public int ImportarDesdeAccess(string rutaAccess, string nombreSede)
        {
            // Leer datos desde Access
            var dtAccess = LeerDatosAccess(rutaAccess);

            // Insertar cada registro en SQL Server
            int registrosImportados = 0;
            foreach (DataRow row in dtAccess.Rows)
            {
                string codigoEmpleado = row["CodigoEmpleado"].ToString();
                DateTime fecha = Convert.ToDateTime(row["Fecha"]);
                TimeSpan hora = TimeSpan.Parse(row["Hora"].ToString());

                _asistenciaRepo.InsertarMarcacion(codigoEmpleado, fecha, hora, nombreSede);
                registrosImportados++;
            }

            return registrosImportados;
        }

        /// <summary>
        /// Lee los datos de marcaciones desde una base de datos Access.
        /// Método extraído para cumplir SRP (separar lectura de escritura).
        /// </summary>
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

        // ================================================================
        // USO: Ahora para importar de cualquier sede, se llama así:
        //
        //   servicio.ImportarDesdeAccess(@"\\servidor\asistencias_sede.mdb", "SEDE");
        //   servicio.ImportarDesdeAccess(@"\\servidor\asistencias_consejo.mdb", "CONSEJO");
        //   servicio.ImportarDesdeAccess(@"\\servidor\asistencias_proind.mdb", "PROIND");
        //   servicio.ImportarDesdeAccess(@"\\servidor\asistencias_nosede.mdb", "NOSEDE");
        //
        // Si mañana se agrega una NUEVA SEDE, solo se llama con los nuevos
        // parámetros. NO se necesita crear un nuevo método.
        // ================================================================
    }
}
