// ============================================================================
// v3.0 - REFACTORIZACIÓN SEMANA 5: Principio Abierto-Cerrado (OCP)
// Archivo: Importers/ImporterFactory.cs
// ANTES: En frmPrincipal_Original.vb cada sede tenía su propio event handler
//        que llamaba a un método específico. Para agregar una sede o un nuevo
//        formato, había que modificar el formulario Y ClassRRHH.
// AHORA: Factory que resuelve el importador correcto según la fuente.
//        OCP: Agregar un nuevo formato solo requiere crear la clase y
//        registrarla aquí. El resto del sistema no cambia.
// ============================================================================

using System;
using System.Collections.Generic;
using RRHH.Interfaces;

namespace RRHH.Importers
{
    /// <summary>
    /// Fábrica de importadores de asistencias.
    /// OCP: Registra nuevos importadores sin modificar la lógica del sistema.
    /// Patrón Factory + Strategy combinados.
    /// </summary>
    public class ImporterFactory
    {
        private readonly List<IAsistenciaImporter> _importadores = new List<IAsistenciaImporter>();

        /// <summary>
        /// Registra un nuevo importador en la fábrica.
        /// </summary>
        public void Registrar(IAsistenciaImporter importador)
        {
            _importadores.Add(importador);
        }

        /// <summary>
        /// Obtiene el importador adecuado según la ruta del archivo.
        /// OCP: No necesita if/else por cada tipo. Los importadores se auto-evalúan.
        /// </summary>
        public IAsistenciaImporter ObtenerImportador(string rutaOrigen)
        {
            foreach (var importador in _importadores)
            {
                if (importador.PuedeImportar(rutaOrigen))
                    return importador;
            }

            throw new NotSupportedException(
                $"No se encontró un importador compatible para: {rutaOrigen}");
        }

        /// <summary>
        /// Lista todos los importadores disponibles.
        /// </summary>
        public IReadOnlyList<IAsistenciaImporter> ObtenerTodos()
        {
            return _importadores.AsReadOnly();
        }

        // ================================================================
        // EJEMPLO DE USO EN EL FORMULARIO REFACTORIZADO:
        //
        //   // Configuración inicial (una sola vez)
        //   var factory = new ImporterFactory();
        //   factory.Registrar(new AccessImporter(repo, rutaAccess));
        //   factory.Registrar(new CsvImporter(repo, rutaCsv));
        //   // Si mañana se necesita Excel:
        //   // factory.Registrar(new ExcelImporter(repo, rutaExcel));
        //
        //   // Al importar: el factory elige el importador correcto
        //   var importador = factory.ObtenerImportador(archivoSeleccionado);
        //   int registros = importador.Importar("SEDE");
        //
        // ANTES (código original):
        //   If sede = "SEDE" Then objRRHH.Access2Sql()
        //   ElseIf sede = "CONSEJO" Then objRRHH.Access2SqlCONSEJO()
        //   ElseIf sede = "PROIND" Then objRRHH.Access2SqlPROIND()
        //   ElseIf sede = "NOSEDE" Then objRRHH.Access2SqlSEDE()
        //   ' ← Si se agrega nueva sede = modificar este bloque (viola OCP)
        // ================================================================
    }
}
