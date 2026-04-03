import streamlit as st
import pandas as pd
import plotly.express as px

def salario(Datos_para_pestaña):
    
    #llamamos la funcion data
    resumen_dataset = Datos_para_pestaña

    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        promedio_total = resumen_dataset['salary_usd'].mean()
        st.metric("Promedio Global", f"{promedio_total:,.2f} USD")
        
    with m2:
        mediana_total = resumen_dataset['salary_usd'].median()
        st.metric("Mediana Global", f"{mediana_total:,.2f} USD")
        
    with m3:
        desviacion_total = resumen_dataset['salary_usd'].std()
        st.metric("Desviación Estándar", f"{desviacion_total:,.2f} USD")

    with m4:
        coeficiente_variacion = float(resumen_dataset['salary_usd'].std() / resumen_dataset['salary_usd'].mean()) * 100
        st.metric("Coeficiente de Variación", f"{coeficiente_variacion:,.2f} %")

    st.divider()

    #------Tabla de estadistica descriptiva----
    
    st.subheader("Detalle Estadístico por Industria")
    estadisticas_salario = resumen_dataset.groupby('industry')['salary_usd'].agg(['mean', 'median', 'std', lambda x: (x.std() / x.mean()) * 100]).reset_index()
    
    # Creamos las columnas y sus titulos
    estadisticas_salario.columns = ['Industria', 'Promedio (USD)', 'Mediana (USD)', 'Desviación Estándar', 'Coeficiente de Variación (%)']
    
    # Aquí mostramos la tabla que calculaste con .agg()
    st.dataframe(estadisticas_salario.style.format({
        'Promedio (USD)': '{:,.2f}',
        'Mediana (USD)': '{:,.2f}',
        'Desviación Estándar': '{:,.2f}',
        'Coeficiente de Variación (%)': '{:.2f}%'}), use_container_width=True)

    #mensaje informativo sobre cv
    st.info(f"""
    
    1. **Un CV bajo** (ej. < 15%) indica que los salarios en esa industria son muy similares entre sí.
    2. **Un CV alto** (ej. > 30%) sugiere que hay mucha diferencia entre los que ganan poco y los que ganan mucho.
    
    """)

    st.divider()

    mi_color = "#000000"

    df_grafico = estadisticas_salario.sort_values('Promedio (USD)', ascending=False)
    
    fig = px.bar(
            df_grafico,
            x='Industria',
            y='Promedio (USD)',
            title="Salario promedio de las industrias",
            labels={'Promedio (USD)': 'Salario Promedio (USD)', 'Industria': 'Sector'},
            color='Industria', #el color cambia segun el pais
            color_discrete_sequence=px.colors.qualitative.G10
        )
    

    fig.update_layout(
        bargap=0.1,  # CAMBIO: Se usa bargap en lugar de boxgap
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True, # RECOMENDACIÓN: Como ya tienes los nombres en el eje X, la leyenda sobra
        title_font_color=mi_color,
        font=dict(color=mi_color),
        legend=dict(title_font_color=mi_color, # Color del título de la leyenda
        font=dict(color=mi_color),  # Color de los textos de la leyenda
        #bordercolor=mi_color,       # Opcional: borde de la leyenda
        #borderwidth=1
        ))
    
    fig.update_xaxes(
        title_text="Industria", 
        title_font=dict(color=mi_color, size=16), 
        tickfont=dict(color=mi_color),
        showgrid=True,
        gridcolor='rgba(0,0,0,0.1)'
    )

    fig.update_yaxes(
        title_text="Salario (USD)", 
        title_font=dict(color=mi_color, size=16), 
        tickfont=dict(color=mi_color),
        showgrid=True, 
        gridcolor='rgba(0,0,0,0.1)',
        tickprefix="$", # añade signo de dólar
        tickformat=","  # añade separador de miles
    )
    
    
    st.plotly_chart(fig, on_select="ignore", selection_mode="points")

    st.divider()
       
    fig_box = px.box(
        resumen_dataset, 
        x='industry', 
        y='salary_usd', 
        color='industry',
        title="Dispersión Salarial: ¿Dónde hay más variedad de sueldos?",
        color_discrete_sequence=px.colors.qualitative.G10
    )

    fig_box.update_layout(
        bargap=0.1,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        title_font_color=mi_color,
        font=dict(color=mi_color),
        legend=dict(
            title_font_color=mi_color, # Color del título de la leyenda
            font=dict(color=mi_color),  # Color de los textos de la leyenda
        #bordercolor=mi_color,       # Opcional: borde de la leyenda
        #borderwidth=1
        ))

    fig_box.update_xaxes(
        title_text="Industria", 
        title_font=dict(color=mi_color, size=16), 
        tickfont=dict(color=mi_color),
        showgrid=True,
        gridcolor='rgba(0,0,0,0.1)'
    )

    fig_box.update_yaxes(
        title_text="Salario (USD)", 
        title_font=dict(color=mi_color, size=16), 
        tickfont=dict(color=mi_color),
        showgrid=True, 
        gridcolor='rgba(0,0,0,0.1)',
        tickprefix="$", # añade signo de dólar
        tickformat=","  # añade separador de miles
    )

    st.plotly_chart(fig_box, use_container_width=True)


    st.divider()

    st.subheader("Conclusión del Análisis")

    # Extraemos datos para que la conclusión sea inteligente
    industria_max = df_grafico.iloc[0]['Industria']
    salario_max = df_grafico.iloc[0]['Promedio (USD)']

    # Usamos f-strings para insertar los datos en el texto
    st.info(f"""
    **Principales Hallazgos:**

    1. **Líder del Mercado:** La industria de **{industria_max}** presenta el promedio salarial más alto con **${salario_max:,.2f} USD**.

    """)