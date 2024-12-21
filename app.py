import pandas as pd
import streamlit as st
import plotly.express as px

# Ruta del dataset
DATA_PATH = "greenhouse_gas_inventory_data_data.csv"

# Cargar el dataset
data = pd.read_csv(DATA_PATH)

# Simplificar los nombres de las categorías
data["category"] = data["category"].replace({
    "carbon_dioxide_co2_emissions_without_land_use_land_use_change_and_forestry_lulucf_in_kilotonne_co2_equivalent": "CO2 sin uso de suelo",
    "greenhouse_gas_ghgs_emissions_including_indirect_co2_without_lulucf_in_kilotonne_co2_equivalent": "GHG sin LULUCF",
    "methane_ch4_emissions_without_land_use_land_use_change_and_forestry_lulucf_in_kilotonne_co2_equivalent": "Metano sin uso de suelo",
    "nitrous_oxide_n2o_emissions_without_land_use_land_use_change_and_forestry_lulucf_in_kilotonne_co2_equivalent": "Óxido nitroso sin uso de suelo",
    "sulphur_hexafluoride_sf6_emissions_in_kilotonne_co2_equivalent": "Hexafluoruro de azufre"
})

# Título y descripción
st.title("Análisis de Gases de Efecto Invernadero 🌍")
st.markdown("""
Este proyecto utiliza un conjunto de datos sobre **Emisiones Internacionales de Gases de Efecto Invernadero** 
que abarca los niveles globales de emisiones desde **1990 hasta 2017**, proporcionados por las **Naciones Unidas**.

El objetivo de esta aplicación es:
- Ayudar a prever las tendencias de emisiones globales.
- Explorar los diferentes tipos de emisiones a lo largo del tiempo.
- Proporcionar herramientas interactivas para visualizar y analizar las emisiones de dióxido de carbono, metano, óxido nitroso e hidrofluorocarbonos.
""")

# Filtros interactivos
st.sidebar.header("Filtros")

# Filtrar por país
countries = data["country_or_area"].unique()
selected_country = st.sidebar.selectbox("Selecciona un país", countries)

# Filtrar por año
years = sorted(data["year"].unique())
selected_year = st.sidebar.selectbox("Selecciona un año", years)

# Aplicar filtros
filtered_data = data[(data["country_or_area"] == selected_country) & (data["year"] == selected_year)]

st.subheader(f"Análisis de {selected_country} en el año {selected_year}")

# Gráfico de barras de emisiones por categoría
st.markdown("### Emisiones por Categoría")
if not filtered_data.empty:
    emissions_by_category = filtered_data.groupby("category")["value"].sum().reset_index()
    fig = px.bar(
        emissions_by_category,
        x="category",
        y="value",
        title=f"Emisiones por Categoría en {selected_country} ({selected_year})",
        labels={"category": "Categoría", "value": "Emisiones (Toneladas)"},
        text="value",
    )
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(
        xaxis_title="Categoría",
        yaxis_title="Emisiones (Toneladas)",
        xaxis=dict(tickangle=45),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No hay datos disponibles para los filtros seleccionados.")

# Gráfico de línea para tendencias de emisiones
st.markdown("### Tendencia de Emisiones a lo Largo de los Años")
historical_data = data[data["country_or_area"] == selected_country]

if not historical_data.empty:
    trend_fig = px.line(
        historical_data,
        x="year",
        y="value",
        color="category",
        title=f"Tendencia Histórica de Emisiones en {selected_country}",
        labels={"year": "Año", "value": "Emisiones (Toneladas)", "category": "Categoría"},
    )
    trend_fig.update_layout(
        xaxis_title="Año",
        yaxis_title="Emisiones (Toneladas)",
        legend=dict(title="Categorías", font=dict(size=10), orientation="h", x=0, y=-0.3)
    )
    st.plotly_chart(trend_fig, use_container_width=True)
else:
    st.warning("No hay datos históricos disponibles para este país.")
