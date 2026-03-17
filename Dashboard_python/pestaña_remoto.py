import streamlit as st
import pandas as pd
import plotly.express as px

def remoto(Datos_para_pestaña):
    
    #Llamamos la funcion cargar_limpiar_datos as cld del archivo Cargar_datos
    data_remo = Datos_para_pestaña

    st.subheader("Comparativa Salarial: Remoto vs. Presencial")

    
    #creamos la agrupacion de las varibles a analizar
    estadistica_remoto = data_remo.groupby(['industry','remote_option'])['salary_usd'].mean().reset_index()

    # 1. Filtramos los datos (ajusta 'Remote' e 'In-person' según tus datos reales)
    df_si_remote = estadistica_remoto[estadistica_remoto['remote_option'] == 'Yes']
    df_no_remote = estadistica_remoto[estadistica_remoto['remote_option'] == 'No']

    # 2. Preparamos los títulos de las columnas para las tablas
    columnas_finales = ['Industria', 'Salario Promedio (USD)']

    # 2. Creamos dos columnas para mostrar las tablas lado a lado
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Trabajo Remoto**")
        # Cambiamos nombres solo para la visualización
        df_si_display = df_si_remote.rename(columns={
        'industry': 'Industria', 
        'salary_usd': 'Salario Promedio (USD)'
        })
        st.dataframe(
            df_si_display[columnas_finales].style.format({'Salario Promedio (USD)': '{:,.2f} USD'}),
            hide_index=True,
            use_container_width=True
        )

    with col2:
        st.write("**Trabajo Presencial**")
        df_no_display = df_no_remote.rename(columns={
        'industry': 'Industria', 
        'salary_usd': 'Salario Promedio (USD)'
        })
        st.dataframe(
            df_no_display[columnas_finales].style.format({'Salario Promedio (USD)': '{:,.2f} USD'}),
            hide_index=True,
            use_container_width=True
        )

    st.divider()

    #creamos la grafica de barras
    df_grafico = estadistica_remoto.sort_values(['remote_option','industry'], ascending=False)
    
    mi_color = "#000000"

    fig = px.bar(
            df_grafico,
            x='industry',
            y='salary_usd',
            title="Brecha Salarial: Remoto vs. Presencial por Sector",
            labels={'salary_usd':'Salario promedio (USD)','remote_option': 'Trabajo remoto', 'industry': 'Industria'},
            color='remote_option', #el color cambia segun el trabajo remoto
            barmode='group',
            color_discrete_sequence=px.colors.qualitative.G10
        )
    
    fig.update_layout(
        bargap=0.1,
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
        #tickprefix="$", # añade signo de dólar
        tickformat=","  # añade separador de miles
    )
    
    st.plotly_chart(fig, on_select="ignore", selection_mode="points")

    st.divider()

    # --- Sección de Conclusiones ---

    st.subheader("Conclusion del análisis")

    # Calculamos promedios para la conclusión
    prom_remoto = df_si_remote['salary_usd'].mean()
    prom_presencial = df_no_remote['salary_usd'].mean()
    diff_neta = prom_remoto - prom_presencial
    diff_porcentual = (diff_neta / prom_presencial) * 100

    # Usamos un contenedor informativo
    if abs(diff_porcentual) < 5:
        mensaje = "La diferencia salarial es **mínima**, lo que sugiere que el talento se valora por igual sin importar la modalidad del trabajo."
    elif diff_porcentual > 0:
        mensaje = f"El trabajo remoto paga, en promedio, un **{diff_porcentual:.1f}% más** que el presencial."
    else:
        mensaje = f"Existe una penalización promedio del **{abs(diff_porcentual):.1f}%** para posiciones remotas."

    st.info(f"""
    **Resultados Clave:**
    * {mensaje}
    * **Diferencia neta:** ${abs(diff_neta):,.2f} USD.
    * **Observación:** La paridad salarial indica un mercado laboral digital altamente competitivo.
    """)