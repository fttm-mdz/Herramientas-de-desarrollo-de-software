import pandas as pd
import plotly.express as px
import streamlit as st

car_data = pd.read_csv('vehicles_us.csv')

car_data['odometer'] = car_data['odometer'].fillna(0)
car_data['model_year'] = car_data['model_year'].fillna(0).astype(int)
car_data['is_4wd'] = car_data['is_4wd'].fillna(0).astype(int)
car_data['paint_color'] = car_data['paint_color'].fillna('unknown')

st.title('Análisis de anuncios de coches en EE. UU.')

st.markdown(f"""
Este dataset tiene **{car_data.shape[0]:,} anuncios** de vehículos en EE. UU.  
Explora el kilometraje, precio, año y condición de los vehículos.
""")

st.sidebar.header('Filtros')

#Aquí se crearon filtros para poder ver el tipo del vehiculo y los precios para que el cliente elija (basandome en los datos de la tabla de datos)

tipo_vehiculo = st.sidebar.selectbox(
    'Tipo de vehículo',
    ['Todos'] + sorted(car_data['type'].dropna().unique().tolist())
)

condicion = st.sidebar.selectbox(
    'Condición',
    ['Todas'] + sorted(car_data['condition'].dropna().unique().tolist())
)

precio_min, precio_max = int(car_data['price'].min()), int(car_data['price'].max())
precio_rango = st.sidebar.slider(
    'Rango de precio', 
    precio_min, precio_max, 
    (precio_min, precio_max), 
    step=500
)

ano_min, ano_max = int(car_data['model_year'].min()), int(car_data['model_year'].max())
ano_rango = st.sidebar.slider(
    'Rango de año de modelo', 
    ano_min, ano_max, 
    (ano_min, ano_max)
)

filtered_data = car_data.copy()

if tipo_vehiculo != 'Todos':
    filtered_data = filtered_data[filtered_data['type'] == tipo_vehiculo]

if condicion != 'Todas':
    filtered_data = filtered_data[filtered_data['condition'] == condicion]

filtered_data = filtered_data[
    (filtered_data['price'] >= precio_rango[0]) & 
    (filtered_data['price'] <= precio_rango[1]) &
    (filtered_data['model_year'] >= ano_rango[0]) &
    (filtered_data['model_year'] <= ano_rango[1])
]

st.markdown(f"### Resultados filtrados: {filtered_data.shape[0]:,} anuncios")

#Estos son los gráficos 

if st.checkbox('Mostrar histograma del odómetro'):
    fig_hist = px.histogram(
        filtered_data, 
        x='odometer', 
        nbins=40, 
        title='Distribución del kilometraje',
        color_discrete_sequence=['#636EFA']
    )
    fig_hist.update_layout(template='plotly_white')
    st.plotly_chart(fig_hist, use_container_width=True)

if st.checkbox('Precio vs. kilometraje'):
    fig_scatter = px.scatter(
        filtered_data,
        x='odometer',
        y='price',
        color='condition',
        hover_data=['model', 'model_year', 'type'],
        title='Precio vs. kilometraje según condición',
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig_scatter.update_layout(template='plotly_white')
    st.plotly_chart(fig_scatter, use_container_width=True)

if st.checkbox('Distribución de precio por tipo de vehículo'):
    if filtered_data['type'].nunique() > 1:
        fig_box = px.box(
            filtered_data,
            x='type',
            y='price',
            title='Distribución de precios por tipo de vehículo',
            color='type',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_box.update_layout(template='plotly_white', showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)
    else:
        st.info('Selecciona más de un tipo de vehículo para ver este gráfico.')

if st.checkbox('Conteo de vehículos por condición'):
    cond_counts = filtered_data['condition'].value_counts().reset_index()
    cond_counts.columns = ['Condición', 'Cantidad']
    fig_bar = px.bar(
        cond_counts,
        x='Condición',
        y='Cantidad',
        text='Cantidad',
        title='Cantidad de vehículos por condición',
        color='Condición',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig_bar.update_layout(template='plotly_white')
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown('---')
st.markdown('Creado por Fátima Méndez • Bootcamp de análisis de datos')


