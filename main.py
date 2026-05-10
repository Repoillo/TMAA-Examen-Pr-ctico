import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Analisis Estadistico", layout="centered")

COLOR_PRINCIPAL = '#8B0000'
COLOR_SECUNDARIO = '#DC143C'
COLOR_FONDO_GRAFICA = '#0E1117'

st.title("Examen Práctico: Aves")
st.markdown("---")

try:
    df = pd.read_csv('aves.csv')
except FileNotFoundError:
    st.error("Archivo aves.csv no encontrado en el directorio.")
    st.stop()

seccion = st.selectbox(
    "Seleccione el apartado a visualizar:",
    ("1. Base de Datos", 
     "2. Medidas de Tendencia Central", 
     "3. Distribucion de Frecuencias", 
     "4. Visualizacion Grafica")
)

st.markdown("---")

if seccion == "1. Base de Datos Cruda":
    st.subheader("Registros Recolectados")
    st.dataframe(df, use_container_width=True)

elif seccion == "2. Medidas de Tendencia Central":
    st.subheader("Analisis de Tendencia Central")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Media y Mediana (Variables Cuantitativas)**")
        metricas = df[['peso_kg', 'altura_m', 'velocidad_kmh']].agg(['mean', 'median'])
        st.dataframe(metricas, use_container_width=True)
        
    with col2:
        st.markdown("**Moda (Variables Cuantitativas y Cualitativas)**")
        modas = df[['peso_kg', 'altura_m', 'velocidad_kmh', 'color']].mode().iloc[0]
        st.dataframe(modas.astype(str), use_container_width=True)

elif seccion == "3. Distribucion de Frecuencias":
    st.subheader("Tabla de Frecuencias por Atributo (Color)")
    
    f_abs = df['color'].value_counts()
    f_rel = (f_abs / len(df)) * 100
    f_acum = f_abs.cumsum()
    
    tabla_frec = pd.DataFrame({
        "Frecuencia Absoluta": f_abs,
        "Frecuencia Relativa (%)": f_rel.round(2),
        "Frecuencia Acumulada": f_acum
    })
    
    st.dataframe(tabla_frec, use_container_width=True)

elif seccion == "4. Visualizacion Grafica":
    st.subheader("Representaciones Estadisticas")
    
    f_abs = df['color'].value_counts()
    f_rel = (f_abs / len(df)) * 100
    
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        st.markdown("**Frecuencia Absoluta (Barras)**")
        fig_bar, ax_bar = plt.subplots(figsize=(5, 4))
        fig_bar.patch.set_facecolor(COLOR_FONDO_GRAFICA)
        ax_bar.set_facecolor(COLOR_FONDO_GRAFICA)
        
        f_abs.plot(kind='bar', color=COLOR_PRINCIPAL, ax=ax_bar)
        
        ax_bar.tick_params(colors='white', axis='x', rotation=45)
        ax_bar.tick_params(colors='white', axis='y')
        ax_bar.set_ylabel("Cantidad de Especimenes", color='white')
        for spine in ax_bar.spines.values():
            spine.set_edgecolor('white')
            
        st.pyplot(fig_bar)

    with col_graf2:
        st.markdown("**Frecuencia Relativa (Pastel)**")
        fig_pie, ax_pie = plt.subplots(figsize=(5, 4))
        fig_pie.patch.set_facecolor(COLOR_FONDO_GRAFICA)
        
        colores_pastel = ['#8B0000', '#B22222', '#DC143C', '#CD5C5C', '#F08080']
        
        f_rel.plot(kind='pie', autopct='%1.1f%%', ax=ax_pie, colors=colores_pastel, textprops={'color':"white"})
        ax_pie.set_ylabel("") 
        st.pyplot(fig_pie)

    st.markdown("---")
    st.markdown("**Poligono de Frecuencias (Velocidad)**")
    
    fig_poly, ax_poly = plt.subplots(figsize=(8, 4))
    fig_poly.patch.set_facecolor(COLOR_FONDO_GRAFICA)
    ax_poly.set_facecolor(COLOR_FONDO_GRAFICA)
    
    counts, bin_edges = np.histogram(df['velocidad_kmh'], bins=5)
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    
    ax_poly.plot(bin_centers, counts, marker='o', linestyle='-', color=COLOR_SECUNDARIO, linewidth=2, markersize=6)
    ax_poly.fill_between(bin_centers, counts, color=COLOR_SECUNDARIO, alpha=0.1)
    
    ax_poly.set_xlabel("Velocidad (km/h)", color='white')
    ax_poly.set_ylabel("Frecuencia", color='white')
    ax_poly.tick_params(colors='white')
    for spine in ax_poly.spines.values():
        spine.set_edgecolor('white')
        
    ax_poly.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.3)
    
    st.pyplot(fig_poly)