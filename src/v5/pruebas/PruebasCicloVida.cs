using System;
using System.Data;
using System.Data.SqlClient;
using ClassRRHH;

// Suite propia S09. Solo datos sintéticos y código nuevo/reutilizado del caso.
// El mismo ejecutable se compila por separado contra generadores v4 y v5.
internal static class PruebasCicloVida
{
    private static int _aprobadas;
    private static int _fallidas;

    private sealed class DefinicionEspia : IDefinicionReporte
    {
        private readonly ReporteOficina _original = new ReporteOficina(42);
        public SqlCommand Comando;
        public int Liberaciones;
        public string NombreTabla => _original.NombreTabla;

        public SqlCommand CrearComando(SqlConnection conexion)
        {
            Comando = _original.CrearComando(conexion);
            Comando.Disposed += (sender, args) => { Liberaciones++; };
            return Comando;
        }

        // Limpieza del harness DESPUÉS de observar el comportamiento de Generar.
        public void Limpiar()
        {
            if (Comando != null && Liberaciones == 0) Comando.Dispose();
        }
    }

    private sealed class EjecutorEspia : IEjecutorReportes
    {
        public DefinicionEspia Definicion;
        public DataSet Resultado;
        public Exception Error;
        public int Llamadas;
        public bool DisponibleDurante;

        public DataSet Ejecutar(ComandoReporte reporte)
        {
            Llamadas++;
            DisponibleDurante = Definicion.Liberaciones == 0
                && Object.ReferenceEquals(reporte.Comando, Definicion.Comando)
                && reporte.Comando.CommandType == CommandType.StoredProcedure
                && (int)reporte.Comando.Parameters[0].Value == 42;
            if (Error != null) throw Error;
            return Resultado;
        }
    }

    private static void Comprobar(string nombre, bool condicion)
    {
        if (condicion)
        {
            _aprobadas++;
            Console.WriteLine("PASS:" + nombre);
        }
        else
        {
            _fallidas++;
            Console.WriteLine("FAIL:" + nombre);
        }
    }

    private static void ProbarExito(SqlConnection conexion)
    {
        using (var resultado = new DataSet("datos_sinteticos"))
        {
            var tabla = resultado.Tables.Add("resultado_sintetico");
            tabla.Columns.Add("marca", typeof(string));
            tabla.Rows.Add("RRHH-S09");
            var definicion = new DefinicionEspia();
            var ejecutor = new EjecutorEspia { Definicion = definicion, Resultado = resultado };
            try
            {
                var devuelto = new GeneradorReportes(conexion, ejecutor).Generar(definicion);
                Comprobar("comando_disponible_durante_ejecutor", ejecutor.DisponibleDurante
                    && ejecutor.Llamadas == 1 && conexion.State == ConnectionState.Closed);
                Comprobar("comando_liberado_tras_exito", definicion.Liberaciones == 1);
                Comprobar("dataset_identico_y_utilizable", Object.ReferenceEquals(devuelto, resultado)
                    && (string)devuelto.Tables[0].Rows[0]["marca"] == "RRHH-S09");
            }
            finally { definicion.Limpiar(); }
        }
    }

    private static void ProbarError(SqlConnection conexion)
    {
        var definicion = new DefinicionEspia();
        var esperado = new InvalidOperationException("error sintetico del ejecutor");
        var ejecutor = new EjecutorEspia { Definicion = definicion, Error = esperado };
        Exception recibido = null;
        try
        {
            try { new GeneradorReportes(conexion, ejecutor).Generar(definicion); }
            catch (Exception error) { recibido = error; }
            Comprobar("comando_liberado_tras_error", definicion.Liberaciones == 1);
            Comprobar("misma_excepcion_del_ejecutor", Object.ReferenceEquals(recibido, esperado)
                && ejecutor.Llamadas == 1 && ejecutor.DisponibleDurante
                && conexion.State == ConnectionState.Closed);
        }
        finally { definicion.Limpiar(); }
    }

    private static void ProbarPreparar(SqlConnection conexion)
    {
        var definicion = new DefinicionEspia();
        var ejecutor = new EjecutorEspia { Definicion = definicion };
        ComandoReporte preparado = null;
        try
        {
            preparado = new GeneradorReportes(conexion, ejecutor).Preparar(definicion);
            bool antes = definicion.Liberaciones == 0 && ejecutor.Llamadas == 0
                && Object.ReferenceEquals(preparado.Comando, definicion.Comando)
                && conexion.State == ConnectionState.Closed;
            preparado.Dispose();
            preparado = null;
            Comprobar("preparar_conserva_propiedad_del_llamador", antes && definicion.Liberaciones == 1);
        }
        finally
        {
            if (preparado != null) preparado.Dispose();
            definicion.Limpiar();
        }
    }

    private static int Main()
    {
        using (var conexion = new SqlConnection())
        {
            ProbarExito(conexion);
            ProbarError(conexion);
            ProbarPreparar(conexion);
        }
        Console.WriteLine("LIFECYCLE_SCENARIOS_PASSED=" + _aprobadas);
        Console.WriteLine("LIFECYCLE_SCENARIOS_FAILED=" + _fallidas);
        return _fallidas == 0 ? 0 : 1;
    }
}
