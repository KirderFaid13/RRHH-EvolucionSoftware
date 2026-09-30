using System;
using System.Data;
using System.Data.OleDb;
using System.Data.SqlClient;
using ClassRRHH.My;
using GRLL.Common;
using Microsoft.VisualBasic.CompilerServices;
using Seguridad;

namespace ClassRRHH;

public class AsistenciaAccess
{
	public string BD;

	public string BDProind;

	public string BDConsejo;

	private OleDbConnection oCnAccess;

	private OleDbConnection oCnAccessAlt;

	private SqlConnection ObjCnn;

	public AsistenciaAccess()
	{
		BD = global::Seguridad.Seguridad.DecryptString(MySettingsProperty.Settings.Aplicacion.ToString(), "E");
		BDProind = global::Seguridad.Seguridad.DecryptString(MySettingsProperty.Settings.Key.ToString(), "E");
		BDConsejo = global::Seguridad.Seguridad.DecryptString(MySettingsProperty.Settings.App.ToString(), "E");
		oCnAccess = new OleDbConnection("Provider=Microsoft.Jet.OLEDB.4.0;Data Source=" + BD + "\\Marcacion.mdb;Jet OLEDB:Database Password=" + global::Seguridad.Seguridad.DecryptString(MySettingsProperty.Settings.Serie.ToString(), "E") + ";");
		oCnAccessAlt = new OleDbConnection("Provider=Microsoft.Jet.OLEDB.4.0;Data Source=" + global::Seguridad.Seguridad.DecryptString(MySettingsProperty.Settings.Version.ToString(), "E") + "\\Marcacion.mdb;Jet OLEDB:Database Password=" + global::Seguridad.Seguridad.DecryptString(MySettingsProperty.Settings.SEDE.ToString(), "E") + ";");
		ObjCnn = clsConexion.Conexion;
	}

	public bool Grabar_Asis_Norm(int Pers_DNI, string Fec_Asi, string Hor_Ent, string Hor_Sal, string Alm_Ent, string Alm_Sal)
	{
		oCnAccess.Open();
		OleDbCommand oleDbCommand = new OleDbCommand("SELECT pers_cod from empleado where pers_dni='" + Conversions.ToString(Pers_DNI) + "'", oCnAccess);
		oleDbCommand.CommandType = CommandType.Text;
		OleDbDataAdapter oleDbDataAdapter = new OleDbDataAdapter();
		oleDbDataAdapter.SelectCommand = oleDbCommand;
		DataTable dataTable = new DataTable();
		oleDbDataAdapter.Fill(dataTable);
		if (ExistAsistencia(Conversions.ToInteger(dataTable.Rows[0]["pers_cod"].ToString()), Fec_Asi))
		{
			return false;
		}
		OleDbCommand oleDbCommand2 = new OleDbCommand("INSERT into Asis_Norm (Pers_Cod, Fec_Asi, Hor_Ent, Hor_Sal,Alm_Ent,Alm_Sal) VALUES(" + dataTable.Rows[0]["pers_cod"].ToString() + ",'" + Fec_Asi + "','" + Hor_Ent + "', '" + Hor_Sal + "','" + Alm_Ent + "','" + Alm_Sal + "')", oCnAccess);
		oleDbCommand2.CommandType = CommandType.Text;
		oleDbCommand2.ExecuteNonQuery();
		oCnAccess.Close();
		if (MySettingsProperty.Settings.Aplicacion.ToString().Length >= 3)
		{
			oCnAccessAlt.Open();
			OleDbCommand oleDbCommand3 = new OleDbCommand("INSERT into Asis_Norm (Pers_Cod, Fec_Asi, Hor_Ent, Hor_Sal,Alm_Ent,Alm_Sal) VALUES(" + dataTable.Rows[0]["pers_cod"].ToString() + ",'" + Fec_Asi + "','" + Hor_Ent + "', '" + Hor_Sal + "','" + Alm_Ent + "','" + Alm_Sal + "')", oCnAccessAlt);
			oleDbCommand3.CommandType = CommandType.Text;
			oleDbCommand3.ExecuteNonQuery();
			oCnAccessAlt.Close();
		}
		return true;
	}

	public bool ExistAsistencia(int Pers_Cod, string Fecha)
	{
		DataTable dataTable = new DataTable();
		OleDbCommand oleDbCommand = new OleDbCommand("Select Pers_Cod, Hor_Ent, Hor_Sal FROM Asis_Norm WHERE Pers_Cod = " + Conversions.ToString(Pers_Cod) + " AND Fec_Asi = '" + Fecha + "';", oCnAccess);
		oleDbCommand.CommandType = CommandType.Text;
		OleDbDataAdapter oleDbDataAdapter = new OleDbDataAdapter();
		oleDbDataAdapter.SelectCommand = oleDbCommand;
		oleDbDataAdapter.Fill(dataTable);
		if (dataTable.Rows.Count >= 1)
		{
			return true;
		}
		return false;
	}

	public bool Grabar_Marcaciones(string fecha, string dni, string estado, int proceso, string Lugar)
	{
		oCnAccess.Open();
		OleDbCommand oleDbCommand = new OleDbCommand("Insert into Marcacion (Fecha, Valor, Estado, Proceso, Lugar) VALUES ('" + fecha + "' , '" + dni + "' , '" + estado + "' ," + Conversions.ToString(proceso) + ", '" + Lugar + "');", oCnAccess);
		oleDbCommand.CommandType = CommandType.Text;
		oleDbCommand.ExecuteNonQuery();
		oCnAccess.Close();
		if (MySettingsProperty.Settings.Aplicacion.ToString().Length >= 3)
		{
			oCnAccessAlt.Open();
			OleDbCommand oleDbCommand2 = new OleDbCommand("Insert into Marcacion (Fecha, Valor, Estado, Proceso, Lugar) VALUES ('" + fecha + "' , '" + dni + "' , '" + estado + "' ," + Conversions.ToString(proceso) + ", '" + Lugar + "');", oCnAccessAlt);
			oleDbCommand2.CommandType = CommandType.Text;
			oleDbCommand2.ExecuteNonQuery();
			oCnAccessAlt.Close();
		}
		return true;
	}

	public bool Actualizar_Empleado_Horario(int idhorario, string dni)
	{
		if (oCnAccess.State == ConnectionState.Closed)
		{
			oCnAccess.Open();
		}
		OleDbCommand oleDbCommand = new OleDbCommand("Update Empleado set idHorario=" + Conversions.ToString(idhorario) + " where pers_estado=true and pers_DNI='" + dni.Trim() + "'; ", oCnAccess);
		oleDbCommand.CommandType = CommandType.Text;
		oleDbCommand.ExecuteNonQuery();
		if (oCnAccess.State == ConnectionState.Open)
		{
			oCnAccess.Close();
		}
		if (MySettingsProperty.Settings.Aplicacion.ToString().Length >= 3)
		{
			oCnAccessAlt.Open();
			OleDbCommand oleDbCommand2 = new OleDbCommand("Update Empleado set idHorario=" + Conversions.ToString(idhorario) + " where pers_estado=true and pers_DNI='" + dni.Trim() + "'; ", oCnAccessAlt);
			oleDbCommand2.CommandType = CommandType.Text;
			oleDbCommand2.ExecuteNonQuery();
			oCnAccessAlt.Close();
		}
		return true;
	}

	public object Grabar_suspencion(string Dni, string Fecha)
	{
		if (oCnAccess.State == ConnectionState.Closed)
		{
			oCnAccess.Open();
		}
		DataTable dataTable = new DataTable();
		OleDbCommand oleDbCommand = new OleDbCommand("Select pers_cod from Empleado where pers_estado=true and pers_dni='" + Dni.Trim() + "';", oCnAccess);
		oleDbCommand.CommandType = CommandType.Text;
		OleDbDataAdapter oleDbDataAdapter = new OleDbDataAdapter();
		oleDbDataAdapter.SelectCommand = oleDbCommand;
		oleDbDataAdapter.Fill(dataTable);
		OleDbCommand oleDbCommand2 = new OleDbCommand("Select Count(Pers_Cod) FROM Asis_Norm WHERE Pers_Cod = " + dataTable.Rows[0]["pers_cod"].ToString() + " AND Fec_Asi = '" + Fecha + "';", oCnAccess);
		oleDbCommand2.CommandType = CommandType.Text;
		int num = Conversions.ToInteger(oleDbCommand2.ExecuteScalar());
		checked
		{
			if (num == 1)
			{
				oleDbCommand2.CommandText = "Update Asis_Norm set Suspendido=true where Pers_Cod = " + dataTable.Rows[0]["pers_cod"].ToString() + " AND Fec_Asi = '" + Fecha + "';";
				short num2 = (short)oleDbCommand2.ExecuteNonQuery();
				if (num2 <= 0)
				{
					return false;
				}
			}
			else
			{
				oleDbCommand2.CommandText = "INSERT into Asis_Norm (Pers_Cod, Fec_Asi, Hor_Ent, Hor_Sal,Alm_Ent,Alm_Sal, suspendido) VALUES(" + dataTable.Rows[0]["pers_cod"].ToString() + ",'" + Fecha + "','00:00:00', '00:00:00','00:00:00','00:00:00',true);";
				short num3 = (short)oleDbCommand2.ExecuteNonQuery();
				if (num3 <= 0)
				{
					return false;
				}
			}
			return true;
		}
	}

	public bool Grabar_SalidaAutorizada(string Dni, int NPermiso, string FechaInicio, string FechaFin, bool dia, bool Retorno, string Lugar)
	{
		if (oCnAccess.State == ConnectionState.Closed)
		{
			oCnAccess.Open();
		}
		DataTable dataTable = new DataTable();
		OleDbCommand oleDbCommand = new OleDbCommand("Select pers_cod from Empleado where pers_estado=true and pers_dni='" + Dni.Trim() + "';", oCnAccess);
		oleDbCommand.CommandType = CommandType.Text;
		OleDbDataAdapter oleDbDataAdapter = new OleDbDataAdapter();
		oleDbDataAdapter.SelectCommand = oleDbCommand;
		oleDbDataAdapter.Fill(dataTable);
		oleDbCommand.CommandText = "Insert into Permiso (idEmpleado, NPermiso, FechaInicio, FechaFin, dia,Retorno,Lugar) VALUES (" + dataTable.Rows[0]["pers_cod"].ToString() + " , " + Conversions.ToString(NPermiso) + " , '" + FechaInicio + "' , '" + FechaFin + "' , " + Conversions.ToString(dia) + " , " + Conversions.ToString(Retorno) + " , '" + Lugar + "');";
		short num = checked((short)oleDbCommand.ExecuteNonQuery());
		if (oCnAccess.State == ConnectionState.Open)
		{
			oCnAccess.Close();
		}
		if (num <= 0)
		{
			return false;
		}
		if (MySettingsProperty.Settings.Aplicacion.ToString().Length >= 3)
		{
			if (oCnAccessAlt.State == ConnectionState.Closed)
			{
				oCnAccessAlt.Open();
			}
			OleDbCommand oleDbCommand2 = new OleDbCommand("Insert into Permiso (idEmpleado, NPermiso, FechaInicio, FechaFin, dia,Retorno,Lugar) VALUES (" + dataTable.Rows[0]["pers_cod"].ToString() + " , " + Conversions.ToString(NPermiso) + " , '" + FechaInicio + "' , '" + FechaFin + "' , " + Conversions.ToString(dia) + " , " + Conversions.ToString(Retorno) + " , '" + Lugar + "');", oCnAccessAlt);
			oleDbCommand2.CommandType = CommandType.Text;
			oleDbCommand2.ExecuteNonQuery();
			if (oCnAccessAlt.State == ConnectionState.Open)
			{
				oCnAccessAlt.Close();
			}
		}
		return true;
	}

	public bool Access2Sql(string FechaInicial, string FechaFinal, int forzar)
	{
		oCnAccess.ConnectionString = "Provider=Microsoft.Jet.OLEDB.4.0;Data Source=" + BD + ";Jet OLEDB:Database Password=" + global::Seguridad.Seguridad.DecryptString(MySettingsProperty.Settings.Serie.ToString(), "E") + ";";
		if (oCnAccess.State == ConnectionState.Closed)
		{
			oCnAccess.Open();
		}
		OleDbCommand oleDbCommand = new OleDbCommand("select 'Exec SpRRHH_Asistencia_Import '&''''&e.pers_DNI&''', '''&a.fec_asi&''', '''&a.hor_ent&''', '''&a.hor_sal&''', '''&a.alm_ent&''', '''&a.alm_sal&''','''&a.idhorario& ''' ,  '''&a.estado& ''' , " + Conversions.ToString(forzar) + "' from empleado e inner join asis_norm a on e.pers_cod=a.pers_cod where a.fec_asi >= '" + FechaInicial + "' and a.fec_asi <= '" + FechaFinal + "'", oCnAccess);
		oleDbCommand.CommandType = CommandType.Text;
		OleDbDataAdapter oleDbDataAdapter = new OleDbDataAdapter();
		oleDbDataAdapter.SelectCommand = oleDbCommand;
		DataTable dataTable = new DataTable();
		oleDbDataAdapter.Fill(dataTable);
		if (ObjCnn.State == ConnectionState.Closed)
		{
			ObjCnn.Open();
		}
		bool result;
		try
		{
			foreach (DataRow row in dataTable.Rows)
			{
				SqlCommand sqlCommand = new SqlCommand(row.ItemArray[0].ToString(), ObjCnn);
				sqlCommand.ExecuteNonQuery();
			}
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			result = false;
			ProjectData.ClearProjectError();
			goto IL_0312;
		}
		oleDbCommand.Connection = oCnAccess;
		oleDbCommand.CommandText = "select 'Exec SpRRHH_Marcacion_Import '''&Valor&''', '''&Fecha&''', '''&Estado&''', '''&Lugar&''' , " + Conversions.ToString(forzar) + "' from marcacion where Fecha >= '" + FechaInicial + " 00:00:00' and Fecha < '" + FechaFinal + " 23:59:59' order by Fecha";
		oleDbCommand.CommandType = CommandType.Text;
		oleDbDataAdapter.SelectCommand = oleDbCommand;
		DataTable dataTable2 = new DataTable();
		oleDbDataAdapter.Fill(dataTable2);
		try
		{
			foreach (DataRow row2 in dataTable2.Rows)
			{
				SqlCommand sqlCommand2 = new SqlCommand(row2.ItemArray[0].ToString(), ObjCnn);
				sqlCommand2.ExecuteNonQuery();
			}
		}
		catch (Exception ex3)
		{
			ProjectData.SetProjectError(ex3);
			Exception ex4 = ex3;
			result = false;
			ProjectData.ClearProjectError();
			goto IL_0312;
		}
		if (oCnAccess.State == ConnectionState.Open)
		{
			oCnAccess.Close();
		}
		if (ObjCnn.State == ConnectionState.Open)
		{
			ObjCnn.Close();
		}
		result = true;
		goto IL_0312;
		IL_0312:
		return result;
	}

	public bool Access2SqlSEDE(string FechaInicial, string FechaFinal, int forzar)
	{
		if (oCnAccess.State == ConnectionState.Closed)
		{
			oCnAccess.Open();
		}
		OleDbCommand oleDbCommand = new OleDbCommand("select 'Exec SpRRHH_Asistencia_Import '&''''&e.pers_DNI&''', '''&a.fec_asi&''', '''&a.hor_ent&''', '''&a.hor_sal&''', '''&a.alm_ent&''', '''&a.alm_sal&''', '''&a.idhorario& ''' , '''&a.estado& ''' , " + Conversions.ToString(forzar) + "' from empleado e inner join asis_norm a on e.pers_cod=a.pers_cod where a.fec_asi >= '" + FechaInicial + "' and a.fec_asi <= '" + FechaFinal + "'", oCnAccess);
		oleDbCommand.CommandType = CommandType.Text;
		OleDbDataAdapter oleDbDataAdapter = new OleDbDataAdapter();
		oleDbDataAdapter.SelectCommand = oleDbCommand;
		DataTable dataTable = new DataTable();
		oleDbDataAdapter.Fill(dataTable);
		if (ObjCnn.State == ConnectionState.Closed)
		{
			ObjCnn.Open();
		}
		bool result;
		try
		{
			foreach (DataRow row in dataTable.Rows)
			{
				SqlCommand sqlCommand = new SqlCommand(row.ItemArray[0].ToString(), ObjCnn);
				sqlCommand.ExecuteNonQuery();
			}
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			result = false;
			ProjectData.ClearProjectError();
			goto IL_02af;
		}
		oleDbCommand.Connection = oCnAccess;
		oleDbCommand.CommandText = "select 'Exec SpRRHH_Marcacion_Import '''&Valor&''', '''&Fecha&''', '''&Estado&''', '''&Lugar&''' , " + Conversions.ToString(forzar) + "' from marcacion where Fecha >= '" + FechaInicial + " 00:00:00' and Fecha < '" + FechaFinal + " 23:59:59' order by Fecha";
		oleDbCommand.CommandType = CommandType.Text;
		oleDbDataAdapter.SelectCommand = oleDbCommand;
		DataTable dataTable2 = new DataTable();
		oleDbDataAdapter.Fill(dataTable2);
		try
		{
			foreach (DataRow row2 in dataTable2.Rows)
			{
				SqlCommand sqlCommand2 = new SqlCommand(row2.ItemArray[0].ToString(), ObjCnn);
				sqlCommand2.ExecuteNonQuery();
			}
		}
		catch (Exception ex3)
		{
			ProjectData.SetProjectError(ex3);
			Exception ex4 = ex3;
			result = false;
			ProjectData.ClearProjectError();
			goto IL_02af;
		}
		if (oCnAccess.State == ConnectionState.Open)
		{
			oCnAccess.Close();
		}
		if (ObjCnn.State == ConnectionState.Open)
		{
			ObjCnn.Close();
		}
		result = true;
		goto IL_02af;
		IL_02af:
		return result;
	}

	public bool Access2SqlPROIND(string FechaInicial, string FechaFinal, int forzar)
	{
		oCnAccess.ConnectionString = "Provider=Microsoft.Jet.OLEDB.4.0;Data Source=" + BDProind + "\\Marcacion.mdb;Jet OLEDB:Database Password=" + global::Seguridad.Seguridad.DecryptString(MySettingsProperty.Settings.Serie.ToString(), "E") + ";";
		if (oCnAccess.State == ConnectionState.Closed)
		{
			oCnAccess.Open();
		}
		OleDbCommand oleDbCommand = new OleDbCommand("select 'Exec SpRRHH_Asistencia_Import '&''''&e.pers_DNI&''', '''&a.fec_asi&''', '''&a.hor_ent&''', '''&a.hor_sal&''', '''&a.alm_ent&''', '''&a.alm_sal&''','''&a.idhorario& ''' , '''&a.estado& ''' , " + Conversions.ToString(forzar) + "' from empleado e inner join asis_norm a on e.pers_cod=a.pers_cod where a.fec_asi >= '" + FechaInicial + "' and a.fec_asi <= '" + FechaFinal + "'", oCnAccess);
		oleDbCommand.CommandType = CommandType.Text;
		OleDbDataAdapter oleDbDataAdapter = new OleDbDataAdapter();
		oleDbDataAdapter.SelectCommand = oleDbCommand;
		DataTable dataTable = new DataTable();
		oleDbDataAdapter.Fill(dataTable);
		if (ObjCnn.State == ConnectionState.Closed)
		{
			ObjCnn.Open();
		}
		bool result;
		try
		{
			foreach (DataRow row in dataTable.Rows)
			{
				SqlCommand sqlCommand = new SqlCommand(row.ItemArray[0].ToString(), ObjCnn);
				sqlCommand.ExecuteNonQuery();
			}
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			result = false;
			ProjectData.ClearProjectError();
			goto IL_0312;
		}
		oleDbCommand.Connection = oCnAccess;
		oleDbCommand.CommandText = "select 'Exec SpRRHH_Marcacion_Import '''&Valor&''', '''&Fecha&''', '''&Estado&''', '''&Lugar&''' , " + Conversions.ToString(forzar) + "' from marcacion where Fecha >= '" + FechaInicial + " 00:00:00' and Fecha < '" + FechaFinal + " 23:59:59' order by Fecha";
		oleDbCommand.CommandType = CommandType.Text;
		oleDbDataAdapter.SelectCommand = oleDbCommand;
		DataTable dataTable2 = new DataTable();
		oleDbDataAdapter.Fill(dataTable2);
		try
		{
			foreach (DataRow row2 in dataTable2.Rows)
			{
				SqlCommand sqlCommand2 = new SqlCommand(row2.ItemArray[0].ToString(), ObjCnn);
				sqlCommand2.ExecuteNonQuery();
			}
		}
		catch (Exception ex3)
		{
			ProjectData.SetProjectError(ex3);
			Exception ex4 = ex3;
			result = false;
			ProjectData.ClearProjectError();
			goto IL_0312;
		}
		if (oCnAccess.State == ConnectionState.Open)
		{
			oCnAccess.Close();
		}
		if (ObjCnn.State == ConnectionState.Open)
		{
			ObjCnn.Close();
		}
		result = true;
		goto IL_0312;
		IL_0312:
		return result;
	}

	public bool Access2SqlCONSEJO(string FechaInicial, string FechaFinal, int forzar)
	{
		oCnAccess.ConnectionString = "Provider=Microsoft.Jet.OLEDB.4.0;Data Source=" + BDConsejo + "\\Marcacion.mdb;Jet OLEDB:Database Password=" + global::Seguridad.Seguridad.DecryptString(MySettingsProperty.Settings.Serie.ToString(), "E") + ";";
		if (oCnAccess.State == ConnectionState.Closed)
		{
			oCnAccess.Open();
		}
		OleDbCommand oleDbCommand = new OleDbCommand("select 'Exec SpRRHH_Asistencia_Import '&''''&e.pers_DNI&''', '''&a.fec_asi&''', '''&a.hor_ent&''', '''&a.hor_sal&''', '''&a.alm_ent&''', '''&a.alm_sal&''','''&a.idhorario& ''' , '''&a.estado& ''' , " + Conversions.ToString(forzar) + "' from empleado e inner join asis_norm a on e.pers_cod=a.pers_cod where a.fec_asi >= '" + FechaInicial + "' and a.fec_asi <= '" + FechaFinal + "'", oCnAccess);
		oleDbCommand.CommandType = CommandType.Text;
		OleDbDataAdapter oleDbDataAdapter = new OleDbDataAdapter();
		oleDbDataAdapter.SelectCommand = oleDbCommand;
		DataTable dataTable = new DataTable();
		oleDbDataAdapter.Fill(dataTable);
		if (ObjCnn.State == ConnectionState.Closed)
		{
			ObjCnn.Open();
		}
		bool result;
		try
		{
			foreach (DataRow row in dataTable.Rows)
			{
				SqlCommand sqlCommand = new SqlCommand(row.ItemArray[0].ToString(), ObjCnn);
				sqlCommand.ExecuteNonQuery();
			}
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			result = false;
			ProjectData.ClearProjectError();
			goto IL_0312;
		}
		oleDbCommand.Connection = oCnAccess;
		oleDbCommand.CommandText = "select 'Exec SpRRHH_Marcacion_Import '''&Valor&''', '''&Fecha&''', '''&Estado&''', '''&Lugar&''' , " + Conversions.ToString(forzar) + "' from marcacion where Fecha >= '" + FechaInicial + " 00:00:00' and Fecha < '" + FechaFinal + " 23:59:59' order by Fecha";
		oleDbCommand.CommandType = CommandType.Text;
		oleDbDataAdapter.SelectCommand = oleDbCommand;
		DataTable dataTable2 = new DataTable();
		oleDbDataAdapter.Fill(dataTable2);
		try
		{
			foreach (DataRow row2 in dataTable2.Rows)
			{
				SqlCommand sqlCommand2 = new SqlCommand(row2.ItemArray[0].ToString(), ObjCnn);
				sqlCommand2.ExecuteNonQuery();
			}
		}
		catch (Exception ex3)
		{
			ProjectData.SetProjectError(ex3);
			Exception ex4 = ex3;
			result = false;
			ProjectData.ClearProjectError();
			goto IL_0312;
		}
		if (oCnAccess.State == ConnectionState.Open)
		{
			oCnAccess.Close();
		}
		if (ObjCnn.State == ConnectionState.Open)
		{
			ObjCnn.Close();
		}
		result = true;
		goto IL_0312;
		IL_0312:
		return result;
	}
}
