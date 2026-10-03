using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using ClassRRHH;

// Datos y ejecutores sintéticos de prueba; no representan tablas ni reglas de CMI.
internal partial class PruebasIoC
{
    private static int _escenarios;

    private sealed class EjecutorSimulado : IEjecutorReportes
    {
        public DataSet Resultado;
        public Exception Error;
        public int Llamadas;
        public ComandoReporte Ultimo;

        public DataSet Ejecutar(ComandoReporte reporte)
        {
            Llamadas++;
            Ultimo = reporte;
            if (Error != null) throw Error;
            return Resultado;
        }
    }

    private sealed class DefinicionConError : IDefinicionReporte
    {
        private readonly Exception _error;
        public DefinicionConError(Exception error) { _error = error; }
        public string NombreTabla => "prueba_sintetica";
        public SqlCommand CrearComando(SqlConnection conexion) { throw _error; }
    }

    private static void Require(bool condition)
    {
        if (!condition) throw new Exception("Comportamiento IoC o contrato observado diferente");
    }

    private static void Passed(string name)
    {
        _escenarios++;
        Console.WriteLine("PASS:" + name);
    }

    private static DataSet ResultadoSintetico(string marca)
    {
        var result = new DataSet("datos_sinteticos");
        var table = result.Tables.Add("resultado_sintetico");
        table.Columns.Add("marca", typeof(string));
        table.Rows.Add(marca);
        return result;
    }

    // Las llamadas a este método se generan desde contratos_v1.json, no desde v4.
    private static void Check(GeneradorReportes generator, EjecutorSimulado fake,
                              IDefinicionReporte definition, string sql, string table,
                              string parameter, SqlDbType sqlType, object value,
                              SqlConnection connection, string name)
    {
        int before = fake.Llamadas;
        var result = generator.Generar(definition);
        Require(fake.Llamadas == before + 1 && Object.ReferenceEquals(result, fake.Resultado));
        using (var plan = fake.Ultimo)
        {
            var command = plan.Comando;
            Require(plan.NombreTabla == table && command.CommandText == sql);
            Require(command.CommandType == CommandType.StoredProcedure);
            Require(Object.ReferenceEquals(command.Connection, connection));
            Require(connection.State == ConnectionState.Closed);
            Require(command.Parameters.Count == 1);
            var p = command.Parameters[0];
            Require(p.ParameterName == parameter && p.SqlDbType == sqlType);
            Require(p.Direction == ParameterDirection.Input && Object.Equals(p.Value, value));
            Require(p.Size == (value is string ? ((string)value).Length : 0));
        }
        Passed(name);
    }

    private static void Main()
    {
        using (var connection = new SqlConnection())
        using (var a = ResultadoSintetico("A"))
        using (var b = ResultadoSintetico("B"))
        {
            var fake = new EjecutorSimulado { Resultado = a };
            var generator = new GeneradorReportes(connection, fake);
            Require(fake.Llamadas == 0);
            ProbarContratosRecuperados(generator, fake, connection);

            var other = new EjecutorSimulado { Resultado = b };
            var otherGenerator = new GeneradorReportes(connection, other);
            Require(Object.ReferenceEquals(otherGenerator.Generar(new ReporteOficina(42)), b));
            Require(other.Llamadas == 1 && fake.Llamadas == 11);
            other.Ultimo.Dispose();
            Require(Object.ReferenceEquals(generator.Generar(new ReporteOficina(42)), a));
            Require(fake.Llamadas == 12 && other.Llamadas == 1);
            fake.Ultimo.Dispose();
            Require(connection.State == ConnectionState.Closed);
            Passed("sustitucion_de_ejecutor_y_resultado");

            int before = fake.Llamadas;
            using (var prepared = generator.Preparar(new ReporteOficinaPorSigla("AREA")))
            {
                Require(fake.Llamadas == before && connection.State == ConnectionState.Closed);
                Require(Object.ReferenceEquals(prepared.Comando.Connection, connection));
            }
            Passed("preparar_no_ejecuta_dependencia");

            var expected = new InvalidOperationException("error simulado del ejecutor");
            var failing = new EjecutorSimulado { Error = expected };
            var failingGenerator = new GeneradorReportes(connection, failing);
            Exception caught = null;
            try { failingGenerator.Generar(new ReporteOficina(42)); }
            catch (Exception ex) { caught = ex; }
            Require(Object.ReferenceEquals(caught, expected) && failing.Llamadas == 1);
            Require(connection.State == ConnectionState.Closed);
            failing.Ultimo.Dispose();
            Passed("excepcion_del_ejecutor_se_propaga");

            using (var adapter = new SqlDataAdapter())
            {
                var composed = ComposicionReportes.CrearSql(connection, adapter);
                using (var prepared = composed.Preparar(new ReporteOficina(42)))
                {
                    Require(Object.ReferenceEquals(prepared.Comando.Connection, connection));
                    Require(connection.State == ConnectionState.Closed && adapter.SelectCommand == null);
                    Require((int)prepared.Comando.Parameters[0].Value == 42);
                }
            }
            Passed("composicion_sql_solo_prepara_sin_abrir");

            expected = new InvalidOperationException("error simulado de preparacion");
            caught = null;
            before = fake.Llamadas;
            try { generator.Generar(new DefinicionConError(expected)); }
            catch (Exception ex) { caught = ex; }
            Require(Object.ReferenceEquals(caught, expected) && fake.Llamadas == before);
            Require(connection.State == ConnectionState.Closed);
            Passed("fallo_de_preparacion_no_llama_ejecutor");
        }
        Console.WriteLine("IOC_SCENARIOS_PASSED=" + _escenarios);
    }
}
