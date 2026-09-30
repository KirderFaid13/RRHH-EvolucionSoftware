// ============================================================================
// RECONSTRUCCIÓN POR INGENIERÍA INVERSA - FORMULARIO PRINCIPAL (v1.0)
// Sistema: RecursosHumanos (RRHH) - GRLL 2008
// Archivo: frmPrincipal.vb (Formulario principal de la aplicación)
// PROBLEMAS: Los event handlers contienen lógica de negocio directamente.
//            No hay separación entre presentación y lógica.
// ============================================================================

Imports System.Windows.Forms
Imports DevExpress.XtraBars

Public Class frmPrincipal
    Inherits DevExpress.XtraBars.Ribbon.RibbonForm

    ' PROBLEMA SRP: El formulario accede directamente a ClassRRHH
    ' mezclando la capa de presentación con la de datos
    Private objRRHH As New ClassRRHH()

    Private Sub frmPrincipal_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        ' Configura la conexión directamente en el formulario
        objRRHH.Conexion = My.Settings.CMIConnectionString
        objRRHH.Anio = My.Settings.AnioActual
        CargarListas()
    End Sub

    ' =========================================================================
    ' MENÚ DE ASISTENCIAS - Lógica de negocio en event handlers
    ' PROBLEMA SRP: El formulario decide qué método llamar para cada sede
    ' =========================================================================

    ' PROBLEMA OCP: Si se agrega una nueva sede, hay que agregar un nuevo
    ' menú, un nuevo event handler y un nuevo método en ClassRRHH
    Private Sub ImportarAsistenciasToolStripMenuItem_Click(sender As Object, e As EventArgs)
        ' Importa asistencias de la sede principal
        objRRHH.Access2Sql()  ' Llama directamente al método hardcodeado
        MessageBox.Show("Asistencias importadas correctamente - SEDE")
    End Sub

    Private Sub ImportarAsistenciasCONSEJOToolStripMenuItem_Click(sender As Object, e As EventArgs)
        ' PROBLEMA DRY: Mismo patrón que el anterior, solo cambia el método
        objRRHH.Access2SqlCONSEJO()
        MessageBox.Show("Asistencias importadas correctamente - CONSEJO")
    End Sub

    Private Sub ImportarAsistenciasPROINDToolStripMenuItem_Click(sender As Object, e As EventArgs)
        ' PROBLEMA DRY: Mismo patrón repetido
        objRRHH.Access2SqlPROIND()
        MessageBox.Show("Asistencias importadas correctamente - PROIND")
    End Sub

    Private Sub ImportacionAsistenciasNOSEDEToolStripMenuItem_Click(sender As Object, e As EventArgs)
        ' PROBLEMA DRY: Mismo patrón repetido por cuarta vez
        objRRHH.Access2SqlSEDE()
        MessageBox.Show("Asistencias importadas correctamente - NO SEDE")
    End Sub

    ' =========================================================================
    ' MENÚ DE PERSONAL
    ' =========================================================================

    Private Sub BusquedaToolStripMenuItem_Click(sender As Object, e As EventArgs)
        Dim frm As New frmBuscarPersonas()
        frm.ShowDialog()
    End Sub

    Private Sub CargosToolStripMenuItem_Click(sender As Object, e As EventArgs)
        ' Abre formulario de cargos
    End Sub

    Private Sub MotivoDePermisoToolStripMenuItem_Click(sender As Object, e As EventArgs)
        ' Abre formulario de motivos de permiso
    End Sub

    ' =========================================================================
    ' MENÚ DE REPORTES
    ' PROBLEMA OCP: Cada nuevo reporte requiere un nuevo menú item y handler
    ' =========================================================================

    Private Sub PersonalPorOficinaToolStripMenuItem_Click(sender As Object, e As EventArgs)
        ' Genera reporte de personal por oficina
        objRRHH.Generar_Report_oficina(0)
    End Sub

    Private Sub PersonalPorProfesionToolStripMenuItem_Click(sender As Object, e As EventArgs)
        ' Genera reporte por profesión
        Dim dt As DataTable = objRRHH.ListarProfesiones()
    End Sub

    Private Sub PersonalPorFechaDeIngresoToolStripMenuItem_Click(sender As Object, e As EventArgs)
        ' Genera reporte por fecha de ingreso
    End Sub

    Private Sub EstadisticoPermisosToolStripMenuItem_Click(sender As Object, e As EventArgs)
        ' Genera estadísticas de permisos
    End Sub

    ' =========================================================================
    ' MENÚ DE PLANILLAS
    ' =========================================================================

    Private Sub AsistenciaDiaToolStripMenuItem_Click(sender As Object, e As EventArgs)
        ' Abre formulario de asistencia diaria
    End Sub

    Private Sub RecordAsistenciasSemanalesToolStripMenuItem_Click(sender As Object, e As EventArgs)
        ' Abre formulario de record semanal
    End Sub

    Private Sub AsistenciaDiaSeleccionToolStripMenuItem_Click(sender As Object, e As EventArgs)
        ' Abre formulario de selección de día
    End Sub

    Private Sub CargarListas()
        ' Carga listas de combos y datos iniciales
    End Sub

End Class
