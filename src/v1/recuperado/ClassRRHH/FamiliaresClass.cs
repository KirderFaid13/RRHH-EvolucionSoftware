using System.Data;
using System.Data.SqlClient;
using GRLL.Common;
using Microsoft.VisualBasic.CompilerServices;

namespace ClassRRHH;

public class FamiliaresClass
{
	public SqlConnection ObjCnn;

	public SqlDataAdapter objDA;

	public FamiliaresClass()
	{
		ObjCnn = clsConexion.Conexion;
		objDA = new SqlDataAdapter();
	}

	public object llena_parentezco()
	{
		ObjCnn.Open();
		DataTable dataTable = new DataTable();
		objDA.SelectCommand = new SqlCommand("select IdTipoFam, DescripTipoFam from tipofamiliar", ObjCnn);
		objDA.Fill(dataTable);
		ObjCnn.Close();
		return dataTable;
	}

	public object Busca_DNI(string numDoc, int tipodoc)
	{
		ObjCnn.Open();
		DataTable dataTable = new DataTable();
		objDA.SelectCommand = new SqlCommand("select * from persona where NumDocId='" + numDoc + "'and TipoDocID=" + Conversions.ToString(tipodoc), ObjCnn);
		objDA.Fill(dataTable);
		ObjCnn.Close();
		return dataTable;
	}

	public object Busca_Codigo(int Codper)
	{
		ObjCnn.Open();
		DataTable dataTable = new DataTable();
		objDA.SelectCommand = new SqlCommand("select * from persona inner join familiar on familiar.idpersona=persona.idpersona where persona.IdPersona=" + Conversions.ToString(Codper), ObjCnn);
		objDA.Fill(dataTable);
		ObjCnn.Close();
		return dataTable;
	}
}
