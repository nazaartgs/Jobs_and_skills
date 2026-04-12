import streamlit as st
import pandas as pd
import plotly.express as px

def empresa(Datos_para_pestaña):
    
    df_empresa = Datos_para_pestaña.copy()

 
    col1, col2, col3 = st.columns(3)
    orden_tamaño = ["Small", "Medium", "Large"]

    stats = df_empresa.groupby('company_size')['salary_usd'].agg(['mean', 'median', 'std']).reindex(orden_tamaño)
    stats['CV (%)'] = (stats['std'] / stats['mean']) * 100

    with col1:
        st.metric("Promedio Small", f"${stats.loc['Small', 'mean']:,.0f}")
    with col2:
        st.metric("Promedio Medium", f"${stats.loc['Medium', 'mean']:,.0f}")
    with col3:
        st.metric("Promedio Large", f"${stats.loc['Large', 'mean']:,.0f}")

    st.divider()

    st.subheader("Buscador Personalizado: Empresa e Industria")
    
    c1, c2 = st.columns(2)
    
    with c1:
        tamaños_disponibles = sorted(df_empresa['company_size'].unique())
        size_selected = st.selectbox("Selecciona Tamaño de Empresa", tamaños_disponibles, index=0)

    with c2:

        industrias_filtradas = sorted(df_empresa[df_empresa['company_size'] == size_selected]['industry'].unique())
        ind_selected = st.selectbox("Selecciona la Industria", industrias_filtradas)

    df_filtrado = df_empresa[
        (df_empresa['company_size'] == size_selected) & 
        (df_empresa['industry'] == ind_selected)
    ]

    if not df_filtrado.empty:
        promedio_filtrado = df_filtrado['salary_usd'].mean()
        conteo_vacantes = len(df_filtrado)

        res1, res2 = st.columns(2)
        res1.metric(
            label=f"Salario Promedio ({ind_selected})", 
            value=f"${promedio_filtrado:,.2f} USD"
        )
        res2.metric(
            label="Cantidad de Vacantes", 
            value=conteo_vacantes
        )
    else:
        st.warning("No hay datos para esta combinación específica.")

    st.divider()

    fig_box = px.box(
        df_empresa,
        x="company_size",
        y="salary_usd",
        color="company_size",
        category_orders={"company_size": orden_tamaño},
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
        st.info(f"**Resultado:** No se observa una influencia significativa. La diferencia máxima entre promedios es de solo **${max_diff:,.0f}**, lo que sugiere que el tamaño de la empresa no es un factor determinante.")
    else:
        empresa_top = stats['mean'].idxmax()
        st.success(f"**Resultado:** Se observa una variación de **${max_diff:,.0f}** entre los promedios. Las empresas **{empresa_top}** ofrecen los rangos más competitivos.")

    with st.expander("Ver detalle estadístico"):
        st.table(stats.style.format("${:,.2f}"))