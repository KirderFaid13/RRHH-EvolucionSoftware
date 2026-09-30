// ============================================================================
// RECONSTRUCCIÓN POR INGENIERÍA INVERSA - CÓDIGO ORIGINAL (v1.0)
// Sistema: RecursosHumanos (RRHH) - GRLL 2008
// Archivo: ClassRRHH.vb (Biblioteca de acceso a datos)
// Nota: Reconstruido a partir del análisis de binarios compilados.
//       Este código representa la estructura original del sistema legado.
// ============================================================================
// PROBLEMAS DETECTADOS EN ESTE ARCHIVO:
// 1. VIOLA SRP: Una sola clase maneja empleados, asistencias, permisos,
//    fichas, reportes y planillas. Tiene múltiples razones para cambiar.
// 2. VIOLA DRY: Lógica de conexión a BD repetida en cada método.
//    Métodos Access2Sql* replican la misma lógica para distintas sedes.
// 3. VIOLA OCP: Para agregar nueva sede, se debe crear nuevo método.
//    No hay abstracciones ni interfaces.
// ============================================================================

Imports System.Data
Imports System.Data.SqlClient
Imports System.Data.OleDb

' PROBLEMA SRP: Esta clase tiene DEMASIADAS responsabilidades.
' Maneja empleados, asistencias, permisos, reportes, fichas y planillas
' todo en una sola clase. Cualquier cambio en cualquier módulo afecta a todo.
Public Class ClassRRHH

    ' --- Propiedades (estado global compartido) ---
    Private mCodigoEmpleado As String
    Private mConexion As String
    Private mAnio As String
    Private mSEDE As String
    Private mSerie As String
    Private mAplicacion As String

    Public Property CodigoEmpleado() As String
        Get
            Return mCodigoEmpleado
        End Get
        Set(value As String)
            mCodigoEmpleado = value
        End Set
    End Property

    Public Property Conexion() As String
        Get
            Return mConexion
        End Get
        Set(value As String)
            mConexion = value
        End Set
    End Property

    Public Property Anio() As String
        Get
            Return mAnio
        End Get
        Set(value As String)
            mAnio = value
        End Set
    End Property

    Public Property SEDE() As String
        Get
            Return mSEDE
        End Get
        Set(value As String)
            mSEDE = value
        End Set
    End Property

    ' =========================================================================
    ' MÓDULO 1: GESTIÓN DE EMPLEADOS
    ' PROBLEMA SRP: Debería estar en su propia clase EmpleadoService
    ' =========================================================================

    ' PROBLEMA DRY: La apertura de conexión SQL se repite en TODOS los métodos
    Public Function ObtenerEmpleados() As DataTable
        Dim cn As New SqlConnection(Conexion)
        Dim cmd As New SqlCommand("spRRHH_ListarTrabajadores", cn)
        cmd.CommandType = CommandType.StoredProcedure
        Dim da As New SqlDataAdapter(cmd)
        Dim dt As New DataTable
        cn.Open()
        da.Fill(dt)
        cn.Close()
        Return dt
    End Function

    Public Function BuscarEmpleado_Codigo(ByVal codigo As String) As DataTable
        Dim cn As New SqlConnection(Conexion)  ' DRY: conexión repetida
        Dim cmd As New SqlCommand("spRRHH_ListarTrabajadores", cn)
        cmd.CommandType = CommandType.StoredProcedure
        cmd.Parameters.AddWithValue("@CodigoEmpleado", codigo)
        Dim da As New SqlDataAdapter(cmd)
        Dim dt As New DataTable
        cn.Open()
        da.Fill(dt)
        cn.Close()
        Return dt
    End Function

    Public Sub Ingresa_Empleado(ByVal idEmpleado As Integer, ByVal datos As DataRow)
        Dim cn As New SqlConnection(Conexion)  ' DRY: conexión repetida
        Dim cmd As New SqlCommand("spRRHH_Ingresa_Empleado", cn)
        cmd.CommandType = CommandType.StoredProcedure
        ' ... parámetros del empleado ...
        cn.Open()
        cmd.ExecuteNonQuery()
        cn.Close()
    End Sub

    Public Sub Actualiza_Empleado(ByVal idEmpleado As Integer, ByVal datos As DataRow)
        Dim cn As New SqlConnection(Conexion)  ' DRY: conexión repetida
        Dim cmd As New SqlCommand("spRRHH_Actualiza_Empleado", cn)
        cmd.CommandType = CommandType.StoredProcedure
        ' ... parámetros del empleado ...
        cn.Open()
        cmd.ExecuteNonQuery()
        cn.Close()
    End Sub

    Public Sub Actualizar_Area_Empleado(ByVal idEmpleado As Integer, ByVal idArea As Integer)
        Dim cn As New SqlConnection(Conexion)  ' DRY: conexión repetida
        Dim cmd As New SqlCommand("spRRHH_Actualizar_Area", cn)
        cmd.CommandType = CommandType.StoredProcedure
        cmd.Parameters.AddWithValue("@idEmpleado", idEmpleado)
        cmd.Parameters.AddWithValue("@idArea", idArea)
        cn.Open()
        cmd.ExecuteNonQuery()
        cn.Close()
    End Sub

    Public Function BuscarPersonas(ByVal criterio As String) As DataTable
        Dim cn As New SqlConnection(Conexion)  ' DRY: conexión repetida
        Dim cmd As New SqlCommand("spRRHH_BuscarPersonas", cn)
        cmd.CommandType = CommandType.StoredProcedure
        cmd.Parameters.AddWithValue("@criterio", criterio)
        Dim da As New SqlDataAdapter(cmd)
        Dim dt As New DataTable
        cn.Open()
        da.Fill(dt)
        cn.Close()
        Return dt
    End Function

    ' =========================================================================
    ' MÓDULO 2: GESTIÓN DE ASISTENCIAS
    ' PROBLEMA SRP: Debería estar en su propia clase AsistenciaService
    ' =========================================================================

    Public Function ObtenerAsistenciasxDia(ByVal fecha As Date) As DataTable
        Dim cn As New SqlConnection(Conexion)  ' DRY: conexión repetida
        Dim cmd As New SqlCommand("spRRHH_GetAsistenciaDia", cn)
        cmd.CommandType = CommandType.StoredProcedure
        cmd.Parameters.AddWithValue("@fecha", fecha)
        Dim da As New SqlDataAdapter(cmd)
        Dim dt As New DataTable
        cn.Open()
        da.Fill(dt)
        cn.Close()
        Return dt
    End Function

    Public Sub ActualizaAsistencia(ByVal idEmpleado As Integer, ByVal fecha As Date)
        Dim cn As New SqlConnection(Conexion)  ' DRY: conexión repetida
        Dim cmd As New SqlCommand("spRRHH_ActualizaAsistencia", cn)
        cmd.CommandType = CommandType.StoredProcedure
        cmd.Parameters.AddWithValue("@idEmpleado", idEmpleado)
        cmd.Parameters.AddWithValue("@fecha", fecha)
        cn.Open()
        cmd.ExecuteNonQuery()
        cn.Close()
    End Sub

    Public Function ExisteAsistencia(ByVal idEmpleado As Integer, ByVal fecha As Date) As Boolean
        Dim cn As New SqlConnection(Conexion)  ' DRY: conexión repetida
        Dim cmd As New SqlCommand("spRRHH_ExisteAsistencia", cn)
        cmd.CommandType = CommandType.StoredProcedure
        cmd.Parameters.AddWithValue("@idEmpleado", idEmpleado)
        cmd.Parameters.AddWithValue("@fecha", fecha)
        cn.Open()
        Dim result As Object = cmd.ExecuteScalar()
        cn.Close()
        Return Convert.ToBoolean(result)
    End Function

    Public Sub LlenarPlanillaAsistencia(ByVal anio As String, ByVal mes As String)
        Dim cn As New SqlConnection(Conexion)  ' DRY: conexión repetida
        Dim cmd As New SqlCommand("spRRHH_LlenarPlanillaAsistencia", cn)
        cmd.CommandType = CommandType.StoredProcedure
        cmd.Parameters.AddWithValue("@anio", anio)
        cmd.Parameters.AddWithValue("@mes", mes)
        cn.Open()
        cmd.ExecuteNonQuery()
        cn.Close()
    End Sub

    ' =========================================================================
    ' IMPORTACIÓN DE ASISTENCIAS DESDE ACCESS
    ' PROBLEMA DRY CRÍTICO: Los siguientes 4 métodos hacen EXACTAMENTE lo mismo
    ' pero para distintas sedes. La lógica de lectura de Access, mapeo y 
    ' escritura a SQL Server está DUPLICADA 4 veces.
    ' PROBLEMA OCP: Para agregar una nueva sede, hay que crear un nuevo método
    ' copiando toda la lógica. No está abierto a extensión.
    ' =========================================================================

    Public Sub Access2Sql()
        ' Importa asistencias desde Access (SEDE principal)
        Dim oleConn As New OleDbConnection("Provider=Microsoft.Jet.OLEDB.4.0;Data Source=\\servidor\asistencias_sede.mdb")
        Dim oleCmd As New OleDbCommand("SELECT * FROM Marcaciones", oleConn)
        Dim oleDa As New OleDbDataAdapter(oleCmd)
        Dim dtAccess As New DataTable
        oleConn.Open()
        oleDa.Fill(dtAccess)
        oleConn.Close()

        ' Escribir a SQL Server
        Dim cn As New SqlConnection(Conexion)
        cn.Open()
        For Each row As DataRow In dtAccess.Rows
            Dim cmd As New SqlCommand("spRRHH_InsertarMarcacion", cn)
            cmd.CommandType = CommandType.StoredProcedure
            cmd.Parameters.AddWithValue("@codempleado", row("CodigoEmpleado"))
            cmd.Parameters.AddWithValue("@fecha", row("Fecha"))
            cmd.Parameters.AddWithValue("@hora", row("Hora"))
            cmd.Parameters.AddWithValue("@sede", "SEDE")
            cmd.ExecuteNonQuery()
        Next
        cn.Close()
    End Sub

    ' PROBLEMA DRY: Método casi idéntico a Access2Sql, solo cambia la ruta y el nombre de sede
    Public Sub Access2SqlCONSEJO()
        Dim oleConn As New OleDbConnection("Provider=Microsoft.Jet.OLEDB.4.0;Data Source=\\servidor\asistencias_consejo.mdb")
        Dim oleCmd As New OleDbCommand("SELECT * FROM Marcaciones", oleConn)
        Dim oleDa As New OleDbDataAdapter(oleCmd)
        Dim dtAccess As New DataTable
        oleConn.Open()
        oleDa.Fill(dtAccess)
        oleConn.Close()

        Dim cn As New SqlConnection(Conexion)
        cn.Open()
        For Each row As DataRow In dtAccess.Rows
            Dim cmd As New SqlCommand("spRRHH_InsertarMarcacion", cn)
            cmd.CommandType = CommandType.StoredProcedure
            cmd.Parameters.AddWithValue("@codempleado", row("CodigoEmpleado"))
            cmd.Parameters.AddWithValue("@fecha", row("Fecha"))
            cmd.Parameters.AddWithValue("@hora", row("Hora"))
            cmd.Parameters.AddWithValue("@sede", "CONSEJO")
            cmd.ExecuteNonQuery()
        Next
        cn.Close()
    End Sub

    ' PROBLEMA DRY: Tercer método duplicado, solo cambia ruta y nombre de sede
    Public Sub Access2SqlPROIND()
        Dim oleConn As New OleDbConnection("Provider=Microsoft.Jet.OLEDB.4.0;Data Source=\\servidor\asistencias_proind.mdb")
        Dim oleCmd As New OleDbCommand("SELECT * FROM Marcaciones", oleConn)
        Dim oleDa As New OleDbDataAdapter(oleCmd)
        Dim dtAccess As New DataTable
        oleConn.Open()
        oleDa.Fill(dtAccess)
        oleConn.Close()

        Dim cn As New SqlConnection(Conexion)
        cn.Open()
        For Each row As DataRow In dtAccess.Rows
            Dim cmd As New SqlCommand("spRRHH_InsertarMarcacion", cn)
            cmd.CommandType = CommandType.StoredProcedure
            cmd.Parameters.AddWithValue("@codempleado", row("CodigoEmpleado"))
            cmd.Parameters.AddWithValue("@fecha", row("Fecha"))
            cmd.Parameters.AddWithValue("@hora", row("Hora"))
            cmd.Parameters.AddWithValue("@sede", "PROIND")
            cmd.ExecuteNonQuery()
        Next
        cn.Close()
    End Sub

    ' PROBLEMA DRY: Cuarto método duplicado
    Public Sub Access2SqlSEDE()
        Dim oleConn As New OleDbConnection("Provider=Microsoft.Jet.OLEDB.4.0;Data Source=\\servidor\asistencias_nosede.mdb")
        Dim oleCmd As New OleDbCommand("SELECT * FROM Marcaciones", oleConn)
        Dim oleDa As New OleDbDataAdapter(oleCmd)
        Dim dtAccess As New DataTable
        oleConn.Open()
        oleDa.Fill(dtAccess)
        oleConn.Close()

        Dim cn As New SqlConnection(Conexion)
        cn.Open()
        For Each row As DataRow In dtAccess.Rows
            Dim cmd As New SqlCommand("spRRHH_InsertarMarcacion", cn)
            cmd.CommandType = CommandType.StoredProcedure
            cmd.Parameters.AddWithValue("@codempleado", row("CodigoEmpleado"))
            cmd.Parameters.AddWithValue("@fecha", row("Fecha"))
            cmd.Parameters.AddWithValue("@hora", row("Hora"))
            cmd.Parameters.AddWithValue("@sede", "NOSEDE")
            cmd.ExecuteNonQuery()
        Next
        cn.Close()
    End Sub

    ' =========================================================================
    ' MÓDULO 3: GESTIÓN DE PERMISOS
    ' PROBLEMA SRP: Debería estar en su propia clase PermisoService
    ' =========================================================================

    Public Function ExistePermiso(ByVal idEmpleado As Integer, ByVal fecha As Date) As Boolean
        Dim cn As New SqlConnection(Conexion)  ' DRY: conexión repetida
        Dim cmd As New SqlCommand("spRRHH_ExistePermiso", cn)
        cmd.CommandType = CommandType.StoredProcedure
        cmd.Parameters.AddWithValue("@idEmpleado", idEmpleado)
        cmd.Parameters.AddWithValue("@fecha", fecha)
        cn.Open()
        Dim result As Object = cmd.ExecuteScalar()
        cn.Close()
        Return Convert.ToBoolean(result)
    End Function

    Public Sub ElimnarPermiso(ByVal idPermiso As Integer)
        Dim cn As New SqlConnection(Conexion)  ' DRY: conexión repetida
        Dim cmd As New SqlCommand("spRRHH_EliminarPermiso", cn)
        cmd.CommandType = CommandType.StoredProcedure
        cmd.Parameters.AddWithValue("@idPermiso", idPermiso)
        cn.Open()
        cmd.ExecuteNonQuery()
        cn.Close()
    End Sub

    Public Function SgtIdPermiso() As Integer
        Dim cn As New SqlConnection(Conexion)  ' DRY: conexión repetida
        Dim cmd As New SqlCommand("spRRHH_SgtIdPermiso", cn)
        cmd.CommandType = CommandType.StoredProcedure
        cn.Open()
        Dim result As Object = cmd.ExecuteScalar()
        cn.Close()
        Return Convert.ToInt32(result)
    End Function

    ' =========================================================================
    ' MÓDULO 4: REPORTES Y FICHAS
    ' PROBLEMA SRP: Debería estar en su propia clase ReporteService
    ' =========================================================================

    Public Sub Generar_Ficha(ByVal idEmpleado As Integer)
        Dim cn As New SqlConnection(Conexion)  ' DRY: conexión repetida
        ' ... lógica de generación de ficha del empleado ...
        cn.Open()
        ' Múltiples consultas para datos personales, experiencia, estudios, familia
        cn.Close()
    End Sub

    Public Sub Generar_Report_oficina(ByVal idOficina As Integer)
        Dim cn As New SqlConnection(Conexion)  ' DRY: conexión repetida
        Dim cmd As New SqlCommand("spRRHH_Report_Oficina", cn)
        cmd.CommandType = CommandType.StoredProcedure
        cmd.Parameters.AddWithValue("@idOficina", idOficina)
        Dim da As New SqlDataAdapter(cmd)
        Dim dt As New DataTable
        cn.Open()
        da.Fill(dt)
        cn.Close()
    End Sub

    Public Function generar_rep_cargos() As DataTable
        Dim cn As New SqlConnection(Conexion)  ' DRY: conexión repetida
        Dim cmd As New SqlCommand("spRRHH_Rep_cargos", cn)
        cmd.CommandType = CommandType.StoredProcedure
        Dim da As New SqlDataAdapter(cmd)
        Dim dt As New DataTable
        cn.Open()
        da.Fill(dt)
        cn.Close()
        Return dt
    End Function

    Public Function ListarProfesiones() As DataTable
        Dim cn As New SqlConnection(Conexion)  ' DRY: conexión repetida
        Dim cmd As New SqlCommand("spRRHH_Rep_profesion", cn)
        cmd.CommandType = CommandType.StoredProcedure
        Dim da As New SqlDataAdapter(cmd)
        Dim dt As New DataTable
        cn.Open()
        da.Fill(dt)
        cn.Close()
        Return dt
    End Function

    Public Function GetFeriado(ByVal fecha As Date) As Boolean
        Dim cn As New SqlConnection(Conexion)  ' DRY: conexión repetida
        Dim cmd As New SqlCommand("spRRHH_GetFeriado", cn)
        cmd.CommandType = CommandType.StoredProcedure
        cmd.Parameters.AddWithValue("@fecha", fecha)
        cn.Open()
        Dim result As Object = cmd.ExecuteScalar()
        cn.Close()
        Return Convert.ToBoolean(result)
    End Function

End Class

' ============================================================================
' CLASE DE FICHA SOCIAL - También viola SRP mezclando múltiples entidades
' ============================================================================
Public Class FichaSocialClass
    ' Maneja datos de vivienda, familia y salud en una sola clase
    ' Cada una debería tener su propia clase de servicio
End Class
