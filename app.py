import mysql.connector as mysql
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Trabajando con Productos")
st.title("Exploracion de la Data de Productos")
#funcion para obtener la conexion
def get_Conection():
    conexion = mysql.connect( host="localhost",user="root",
                                   password="Mario2026.", database="bd_lavadora" )
    return conexion
conexion=get_Conection()

if conexion.is_connected():
    st.write("Conection co la base de datos Exitosa")
    cursor=conexion.cursor()
    #consultar la base de datos con cliente
    cursor.execute("SELECT * FROM producto")
    resultados=cursor.fetchall()
    df=pd.DataFrame(resultados, columns=[i[0] for i in cursor.description])
    st.header("Tabla de datos del producto")
    st.dataframe(df)
    st.write("Ver la informacion de la tabla ", df.dtypes)
    st.write("Dimension de la tabla ",df.shape)
    st.write("Datos perdidos o faltantes Na ", df.isna().sum())
    st.header("Estadistica de Productos")
    st.write("Exploracion Estadistica de la Tabla de Productos",df.describe().T)
    st.write("Numero de datos nulos ::", df.isnull().sum().sum())
    st.write("Datos nulos ", df[df.isnull().any(axis=1)])
    st.header("Datos Duplicados de la Tabla")
    st.dataframe(df[df.duplicated()])
    df_clean=df.copy()
    st.header("3. Tratar valores faltantes")
 
    # Reemplazar por un valor fijo en columnas de texto que pueden venir vacías
    df_clean["codigo_barra"] = df_clean["codigo_barra"].fillna(0)
    df_clean["descripcion"] = df_clean["descripcion"].fillna(0)
    df_clean["codigo_principal"] = df_clean["codigo_principal"].fillna(0)
    df_clean["ubicacion_texto"] = df_clean["ubicacion_texto"].fillna(0)
    
    # Reemplazar por la media en columnas numéricas (igual que df["Edad"].fillna(df["Edad"].mean()))
    df_clean["stock"].fillna(df_clean["stock"].mean(), inplace=True)
    df_clean["stock_previo"].fillna(df_clean["stock_previo"].mean(), inplace=True)
    df_clean["utilidad"].fillna(df_clean["utilidad"].mean(), inplace=True)
    
    st.write("Valores nulos después del tratamiento:", df_clean.isnull().sum())
    #ver los outlies de la data
    df_clean["costo"] = pd.to_numeric(df_clean["costo"], errors="coerce")
    df_clean["pvp"] = pd.to_numeric(df_clean["pvp"], errors="coerce")
    st.header("Ver los Outliers")
    for columna in ["costo", "pvp"]:
        Q1 = df_clean[columna].quantile(0.25)
        Q3 = df_clean[columna].quantile(0.75)
        IQR = Q3 - Q1
    
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR
        outliers=(df_clean[columna] < limite_inferior) | (df_clean[columna] > limite_superior)
        st.write(outliers)
    # 4) ELIMINAR DUPLICADOS
# --------------------------------------------
    st.header("4. Eliminar duplicados")
    st.write("Duplicados detectados (df.duplicated()):", df_clean.duplicated().sum())
    df_clean = df_clean.drop_duplicates()
    st.write("Filas después de drop_duplicates():", df_clean.shape[0])
    st.header("Ver la distribucion de los precios ...")

    fig = px.histogram(df, x="pvp", nbins=20,
                   title="Distribución de Precios")
    st.plotly_chart(fig, use_container_width=True)
    df_clean.to_csv("Data_productos.csv", index=False)
    
else:
    st.write("Error en la conexion con la base de datos")