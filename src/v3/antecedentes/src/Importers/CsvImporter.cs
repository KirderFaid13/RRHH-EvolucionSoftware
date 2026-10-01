// ============================================================================
// v3.0 - REFACTORIZACIÓN SEMANA 5: Principio Abierto-Cerrado (OCP)
// Archivo: Importers/CsvImporter.cs
// DEMOSTRACIÓN DEL OCP: Esta clase es un ejemplo de EXTENSIÓN.
// Para agregar soporte de importación desde CSV, solo se creó esta NUEVA clase.
// NO se modificó AccessImporter ni ningún código existente.
// Esto demuestra que el diseño está ABIERTO para extensión y CERRADO
// para modificación → cumple el Principio Abierto-Cerrado.
// ============================================================================

using System;
using System.Data;
using System.IO;
using RRHH.Interfaces;
using RRHH.DataAccess;

namespace RRHH.Importers
{
    /// <summary>
    /// Importador de asistencias desde archivos CSV.
    /// OCP DEMOSTRADO: Esta clase se agregó SIN modificar ningún código existente.
    /// Es una EXTENSIÓN pura del sistema.
    /// </summary>
    public class CsvImporter : IAsistenciaImporter
    {
        private readonly AsistenciaRepository _repo;
        private readonly string _rutaCsv;

        public string Nombre => "Importador CSV (.csv)";

        public CsvImporter(AsistenciaRepository repo, string rutaCsv)
        {
            _repo = repo;
            _rutaCsv = rutaCsv;
        }

        public bool PuedeImportar(string rutaOrigen)
        {
            return rutaOrigen.EndsWith(".csv", StringComparison.OrdinalIgnoreCase);
        }

        public int Importar(string sede)
        {
            int registros = 0;
            var lineas = File.ReadAllLines(_rutaCsv);

            // Saltar la cabecera
            for (int i = 1; i < lineas.Length; i++)
            {
                var campos = lineas[i].Split(',');
                if (campos.Length >= 3)
                {
                    _repo.InsertarMarcacion(
                        campos[0].Trim(),                               // CodigoEmpleado
                        DateTime.Parse(campos[1].Trim()),               // Fecha
                        TimeSpan.Parse(campos[2].Trim()),               // Hora
                        sede);
                    registros++;
                }
            }
            return registros;
        }
    }
}
