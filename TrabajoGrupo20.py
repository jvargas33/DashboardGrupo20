#Importamos las bibliotecas necesarias
# En cmd "streamlit run TrabajoGrupo20.py"
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# Configuración básica de la página
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

#Configuración simple para los gráficos
sns.set_style("whitegrid")

#############################
#CARGA DE DATOS
#############################

#Funcion para cargar datos con cache para mejorar rendimiento
@st.cache_data
def cargar_datos():
    df=pd.read_csv("data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

#Cargamos los datos
df=cargar_datos()

###################################################
#CONFIGURACION DE LA BARRA LATERAL
###################################################

#Simplificamos la barra lateral con solo lo esencial
st.sidebar.header("Filtros del Dashboard📊")


#Selector de rango de fecha
fecha_inicio, fecha_final= st.sidebar.slider(
    "Rango de fechas",
    df['Date'].min().date(),
    df['Date'].max().date(),
    value=(df['Date'].min().date(), df['Date'].max().date()),
    format="DD/MM/YYYY"
)



#Filtro de Líneas de Producto
filtro_linea_producto = st.sidebar.multiselect(
    "Líneas de Producto",
    options=['Health and beauty', 'Electronic accessories',
       'Home and lifestyle', 'Sports and travel', 'Food and beverages',
       'Fashion accessories'],
    default=['Health and beauty', 'Electronic accessories',
       'Home and lifestyle', 'Sports and travel', 'Food and beverages',
       'Fashion accessories'],
    help="Selecciona las categorías"
)

#Filtramos los datos según el rango de fecha seleccionado
df_filtrado = df[(df['Date'].dt.date >= fecha_inicio) & (df['Date'].dt.date <= fecha_final)]
#Se filtra los datos para mostrar solo Líneas de Producto seleccionado junto al rango de fecha seleccionado
df_filtrado_LP=df_filtrado[df_filtrado["Product line"].isin(filtro_linea_producto)] 
    

#Título principal del dashboard
st.title("🛒Dashboard Supermarket Sales")
st.write("Powered by Grupo 20")

###################################################
#            SECCIÓN DE GRÁFICOS                  #
###################################################

# Mostramos métricas generales de ventas
st.subheader(f"Métricas de ventas entre {fecha_inicio.strftime('%d/%m/%Y')} y {fecha_final.strftime('%d/%m/%Y')}")

# Creamos tres columnas para las métricas principales
col1, col2, col3 = st.columns(3)

ventas_Totales = df_filtrado["Total"].sum() #Ventas totales con filtro de fecha
unidades_Vendidas = df_filtrado["Quantity"].sum() #Unidades vendidas con filtro de fecha
ventas_Diaria_Promedio = (df_filtrado["Date"].count())/((fecha_final-fecha_inicio).days+1) #Venta diaria promedio con filtro de fecha

# Mostramos las métricas con formato adecuado
col1.metric("Monto Ventas Totales", f"${ventas_Totales:,.2f} ", help=f"Ventas totales en rango de fecha especificado.")
col2.metric("Unidades Vendidas", f"{unidades_Vendidas:,.0f}", help=f"Unidades vendidas en rango de fecha especificado.")
col3.metric("Ventas Diarias Promedio", f"{ventas_Diaria_Promedio:.1f}", help=f"Ventas diarias en rango de fecha especificado.")

####################
####PRIMERA FILA####
####################
#1) Evolución de las ventas totales
st.write("### Evolución de las ventas totales")
#Creación de figura
fig1, ax1 = plt.subplots(figsize=(8, 5))
  
#Graficamos
ventas_diarias = df_filtrado.groupby("Date")["Total"].sum().reset_index()
sns.lineplot(data=ventas_diarias, x="Date", y="Total", ax=ax1)

#Configuración del gráfico
ax1.set_ylabel("Ventas $")
ax1.set_xlabel("Fecha")
plt.setp(ax1.get_xticklabels(), rotation=45)
ax1.grid(True, alpha=0.7)
ax1.xaxis.grid(False)
ax1.set_ylim(0)

#Mostramos el gráfico
st.pyplot(fig1)
st.write("*El gráfico muestra la evolución de las ventas totales en el transcurso del tiempo, sin marcar una tendencia de mayores ventas.")

####################
####SEGUNDA FILA####
####################
#2) Ingreso por Línea de Producto
st.write("### Ingresos por Línea de Producto")

#Condicional para filtrar gráfico por Línea de Producto y fecha
if filtro_linea_producto:
    #Creación de figura
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    
    #Graficamos
    ingresos_por_producto = df_filtrado_LP.groupby("Product line")["Total"].sum().sort_values().reset_index()
    sns.barplot(data=ingresos_por_producto, x="Total", hue="Product line", y="Product line", palette="viridis", ax=ax2, legend=False)
    
    #Configuración del gráfico
    ax2.set_ylabel("Línea de Producto")
    ax2.set_xlabel("Ingresos $")
    ax2.yaxis.grid(False)  # Asegura que no haya líneas horizontales

    #Mostramos el gráfico
    st.pyplot(fig2)
    st.write("*Se observa que los productos en general no presentan grandes diferencias de ingresos, pero los productos de 'Food and beverages' son los que más aportan a los ingresos y los que menos aportan son los de 'Health and beauty'.")
else:
    st.info("Seleccione al menos una Línea de Producto.")

####################
####TERCERA FILA####
####################

#División para los títulos
t1_f3, t2_f3 = st.columns(2)
with t1_f3:
    st.write("### Distribución de Calificación")
with t2_f3:
    st.write("### Comparación Gasto por Tipo de Cliente")
    


#Se divide la fila en 2 columnas
c1_f3, c2_f3 = st.columns(2)

#3)Distribución de la Calificación de Clientes:
with c1_f3:
    #Condicional para filtrar gráfico por Línea de Producto y fecha
    if filtro_linea_producto:
        #Cración de la figura
        fig3, ax3 = plt.subplots(figsize=(8, 5))
        
        #Graficamos
        sns.histplot(df_filtrado_LP["Rating"], bins=10, kde=True, ax=ax3)
        
        #Configuración del gráfico
        ax3.set_title("Distribución de la Calificación de Clientes")
        ax3.set_xlabel("Calificación")
        ax3.set_ylabel("Cantidad")
        ax3.grid(True, alpha=0.7)

        #Mostramos el gráfico
        st.pyplot(fig3)
        st.write("*Se observa que las calificaciones de los usuarios son principalmente positivas, donde la mayor frecuencia se encuentra entre las notas 6 y 7.")
    else:
        st.info("Seleccione al menos una Línea de Producto.")
        
#4)Comparación del Gasto por Tipo de Cliente:
with c2_f3:
    #Condicional para filtrar gráfico por Línea de Producto y fecha
    if filtro_linea_producto:
        #Creación de la figura
        fig4, ax4 = plt.subplots(figsize=(8, 5))
        
        #Graficamos
        sns.boxplot(data=df_filtrado_LP, x="Customer type", hue="Customer type", y="Total", ax=ax4, palette="viridis", legend=False)
        
        #Configuración del gráfico
        ax4.set_title("Comparación del Gasto por Tipo de Cliente")
        ax4.set_ylabel("Gasto")
        ax4.set_xlabel("Tipo de Cliente")
        ax4.set_ylim(0)
        
        #Mostramos el gráfico
        st.pyplot(fig4)
        st.write("*Se observa que ambos grupos de clientes presentan un gasto similar, pero que existen más out layers en el grupo normal, lo que supone que son clientes que se deben captar como miembros.")
    else:
        st.info("Seleccione al menos una Línea de Producto.")

###################
####CUARTA FILA####
###################
#División para los títulos
t1_f4, t2_f4 = st.columns(2)
with t1_f4:
    st.write("### Relación Costo y Ganancia Bruta")
with t2_f4:
    st.write("### Métodos de Pago Preferidos")

#Se divide la fila en 2 columnas
c1_f4, c2_f4 = st.columns(2)

with c1_f4:
    #Condicional para filtrar gráfico por Línea de Producto y fecha
    if filtro_linea_producto:
        #Creación de la figura
        fig5, ax5 = plt.subplots(figsize=(8, 5))
        
        #Graficamos
        sns.scatterplot(data=df_filtrado_LP, x="cogs", y="gross income", ax=ax5)
        
        #Configuración del gráfico
        ax5.set_title("Relación entre Costo y Ganancia Bruta")
        ax5.set_xlim(0)
        ax5.set_ylim(0)
        ax5.set_xlabel("Costo por unidad")
        ax5.set_ylabel("Ganancia Bruta")
        ax5.grid(True, alpha=0.7)
        
        #Mostramos el gráfico
        st.pyplot(fig5)
        st.write("*Se observa que existe una relacion directamente proporcional, entre mayor sea el costo del producto, mayor es la ganancia bruta.")
    else:
        st.info("Seleccione al menos una Línea de Producto.")

with c2_f4:
    #Condicional para filtrar gráfico por Línea de Producto y fecha
    if filtro_linea_producto:
        #Creación de la figura
        fig6, ax6 = plt.subplots(figsize=(8, 5))
        
        #Graficamos
        sns.countplot(data=df_filtrado_LP, x="Payment", hue="Payment",order=df["Payment"].value_counts().index, ax=ax6, palette="viridis", legend=False)
        
        #Configuración del gráfico
        ax6.set_title("Métodos de Pago Preferidos")
        ax6.set_xlabel("Método de Pago")
        ax6.set_ylabel("Cantidad de Compras")
        
        #Mostramos el gráfico
        st.pyplot(fig6)
        st.write("*No existe una preferencia absoluta o marcada por el tipo de pago, sin embargo se aprecia que 'Credit Card' es el medio de pago menos frecuente.")
    else:
        st.info("Seleccione al menos una Línea de Producto.")
###################
####QUINTA FILA####
###################
#Se divide la fila en 2 columnas
t1_f5, t2_f5 = st.columns(2)
with t1_f5:
    st.subheader("Análisis de Correlación Numérica")
with t2_f5:
    st.subheader("Composición Ingreso Bruto por Sucursal y Línea de Producto")
    

c1_f5, c2_f5 = st.columns(2)

with c1_f5:
    #Creación de la figura
    fig7, ax7 = plt.subplots(figsize=(8, 5.5))
    
    #Graficamos
    numeric_columns = ["Unit price", "Quantity", "Tax 5%", "Total", "cogs", "gross income", "Rating"]
    correlation = df[numeric_columns].corr()
    sns.heatmap(correlation, annot=True, cmap="coolwarm", fmt=".2f", ax=ax7)
    
    #Configuración del gráfico
    ax7.set_title("Análisis de Correlación Numérica")
    ax7.set_xticklabels(ax7.get_xticklabels(), rotation=45, ha="right")
    ax7.set_yticklabels(ax7.get_yticklabels(), rotation=0)

    #Mostramos el gráfico
    st.pyplot(fig7)
    st.write("*Se observa que existen 4 variables que están 100% correlacionadas, que son los costos (cogs), utilidad (gross income), precio total e impuesto (Tax). Estas variables a la vez tienen una correlación directa con el precio del producto junto a las unidades vendidas.")

with c2_f5:
    #Condicional para filtrar gráfico por Línea de Producto y fecha
    if filtro_linea_producto:
        #Función para definir color texto
        def color_texto(rgb):
            luz = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
            if luz < 0.5:
                return "white"
            else:
                return "black"
            
        #Creación de la figura
        fig8, ax8 = plt.subplots(figsize=(10,10))
        
        #Graficamos
        data_agrupada = df_filtrado_LP.groupby(["Branch", "Product line"])["gross income"].sum().reset_index()
        tabla_pivote_a = data_agrupada.pivot_table(index="Branch", columns="Product line", values="gross income")

        #Creación de colormap personalizado para posterior asignación de color de etiqueta
        categorias = tabla_pivote_a.columns.tolist()
        cmap = plt.colormaps['viridis'].resampled(len(categorias))
        colores_rgb = []
        for i in range(len(categorias)):
            color = cmap(i)         # Se obtiene color en RGBA
            color_rgb = mcolors.to_rgb(color)  # Conversión a RGB
            colores_rgb.append(color_rgb)
        
        #Graficamos
        tabla_pivote_a.plot(kind="bar", stacked=True, ax=ax8, xlabel="Sucursal", ylabel="Ingreso Bruto $", color=colores_rgb)
        
        #Configuración del gráfico
        ax8.tick_params(axis='x', rotation=0)
        ax8.legend(title="Línea de Producto", bbox_to_anchor=(1, 1), loc='upper left')
        for container, color_rgb in zip(ax8.containers, colores_rgb): 
            colorTexto = color_texto(color_rgb)
            ax8.bar_label(container, fmt='%.2f', label_type='center', color=colorTexto)
        
        st.pyplot(fig8)
        
        #Encontrar sucursal con mayor ingreso bruto
        ingresos_por_sucursal = data_agrupada.groupby("Branch")["gross income"].sum()
        mejor_sucursal = ingresos_por_sucursal.idxmax()
        ingreso_total_mejor_sucursal = ingresos_por_sucursal[mejor_sucursal]

        datos_sucursal = data_agrupada[data_agrupada["Branch"] == mejor_sucursal]
        mejor_linea_producto = datos_sucursal.loc[datos_sucursal["gross income"].idxmax(), "Product line"]
        monto_mejor_linea = datos_sucursal.loc[datos_sucursal["Product line"] == mejor_linea_producto, "gross income"].values[0]
        
        st.write(f"*Se logra apreciar que la sucursal '{mejor_sucursal}' es la que posee un mayor ingreso bruto con un monto de \${ingreso_total_mejor_sucursal:.2f}, en donde la Línea de Producto '{mejor_linea_producto}' posee el mayor retorno de la sucursal por monto de \${monto_mejor_linea:.2f}.")
    else:
        st.info("Seleccione al menos una Línea de Producto.")

# Pie de página simple
st.markdown("---")
st.caption("🛒Dashboard Supermarket Sales Simple | Datos: data.csv")
st.caption("Powered by Grupo 20")