using System.Data;

namespace ClassRRHH;

// Semana 07: permite entregar un ejecutor SQL o un sustituto desde fuera.
public interface IEjecutorReportes
{
    DataSet Ejecutar(ComandoReporte reporte);
}
