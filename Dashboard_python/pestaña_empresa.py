import streamlit as st
import pandas as pd
import plotly.express as px

def empresa(Datos_para_pestaña):
    
    df_empresa = Datos_para_pestaña.copy()

    col1, col2, col3 = st.columns(3)
    
    orden_tamano = ["Small", "Medium", "Large"]

    stats = df_empresa.groupby('company_size')['salary_usd'].agg(['mean', 'median', 'std']).reindex(orden_tamano)

    stats['CV (%)'] = (stats['std'] / stats['mean']) * 100

    with col1:
        st.metric("Promedio Small", f"${stats.loc['Small', 'mean']:,.0f}")
    with col2:
        st.metric("Promedio Medium", f"${stats.loc['Medium', 'mean']:,.0f}")
    with col3:
        st.metric("Promedio Large", f"${stats.loc['Large', 'mean']:,.0f}")

    st.divider()

    fig_box = px.box(
        df_empresa,
        x="company_size",
        y="salary_usd",
        color="company_size",
        category_orders={"company_size": orden_tamano},
        title="Distribución Salarial por Tamaño de Empresa",
        labels={"company_size": "Tamaño de Empresa", "salary_usd": "Salario (USD)"},
        points=False,
        color_discrete_sequence=px.colors.qualitative.Safe
    )

    fig_box.update_layout(
        xaxis_title="Tamaño de la Organización",
        yaxis_title="Salario Anual (USD)",
        showlegend=False
    )

    st.plotly_chart(fig_box, use_container_width=True)

    st.divider()

    st.subheader("Conclusión del Análisis")
    
    max_diff = stats['mean'].max() - stats['mean'].min()
    
    if max_diff < 5000:
        st.info(f"**Resultado:** No se observa una influencia significativa. La diferencia máxima entre promedios es de solo **${max_diff:,.0f}**, lo que sugiere que en este mercado de alta tecnología, el tamaño de la empresa no es un factor determinante para el salario base.")
    else:
        empresa_top = stats['mean'].idxmax()
        st.success(f"**Resultado:** Se observa una variación de **${max_diff:,.0f}** entre los promedios. Las empresas de tamaño **{empresa_top}** tienden a ofrecer los rangos más competitivos.")

    # Tabla comparativa detallada
    with st.expander("Ver detalle estadístico"):
        st.table(stats.style.format("${:,.2f}"))