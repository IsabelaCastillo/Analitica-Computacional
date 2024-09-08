# -*- coding: utf-8 -*-

# Ejecute esta aplicación con 
# python app1.py
# y luego visite el sitio 
# http://127.0.0.1:8050/ 
# en su navegador.

import dash
from dash import dcc  # dash core components
from dash import html # dash html components
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# en este primer ejemplo usamos unos datos de prueba que creamos directamente
# en un dataframe de pandas 
# df = pd.DataFrame({
#     "Fiebre": ["Bajito", "Mas_Bajito", "Super_Alto", "Bajito", "Mas_Bajito", "Super_Alto"],
#     "Casos": [9, 5, 6, 6, 9, 10],
#     "Diagnóstico": ["Positivo", "Positivo", "Positivo", "Negativo", "Negativo", "Negativo"]
# })

# fig = px.bar(df, x="Fiebre", y="Casos", color="Diagnóstico", barmode="group")

# app.layout = html.Div(children=[
#     html.H1(children='Mi primer tablero en Dash'),

#     html.Div(children='''
#         Histograma de casos según síntomas y diagnóstico
#     '''),

#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     ),
#     html.Div(children='''
#         En este gráfico se observa el número de casos positivos y negativos para COVID-19 según síntomas de fiebre.
#     '''),
#     html.Div(
#         className="Columnas",
#         children=[
#             html.Ul(id='my-list', children=[html.Li(i) for i in df.columns])
#         ],
#     )
#     ]
# )

# Lee el archivo CSV y crea un DataFrame
df = pd.read_csv('Grafica3.csv')
import plotly.graph_objects as go
import pandas as pd

# Asegúrate de que la columna de fecha esté en formato datetime
df['Date'] = pd.to_datetime(df['Date'])

# Agregar columnas para el año, mes y día
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day

# Agrupar los datos solo con las columnas numéricas
df_year = df.groupby('Year')[['Utilidad Bruta', 'Utilidad Neta']].sum().reset_index()
df_month = df.groupby(['Year', 'Month'])[['Utilidad Bruta', 'Utilidad Neta']].sum().reset_index()
df_day = df.groupby(['Year', 'Month', 'Day'])[['Utilidad Bruta', 'Utilidad Neta']].sum().reset_index()

# Crear la figura base para el gráfico apilado
fig = go.Figure()

# Agregar las trazas para los años
fig.add_trace(go.Bar(x=df_year['Year'], y=df_year['Utilidad Bruta'], name='Utilidad Bruta', marker_color='blue'))
fig.add_trace(go.Bar(x=df_year['Year'], y=df_year['Utilidad Neta'], name='Utilidad Neta', marker_color='lightblue'))

# Crear las opciones del dropdown para cambiar entre Año, Mes, Día
fig.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                # Opción para agrupar por Año
                dict(label="Año",
                     method="update",
                     args=[{"x": [df_year['Year'], df_year['Year']],
                            "y": [df_year['Utilidad Bruta'], df_year['Utilidad Neta']],
                            "type": "bar"},
                           {"title": "Comparación por Año",
                            "xaxis": {"title": "Año"},
                            "yaxis": {"title": "Utilidad"}}]),
                # Opción para agrupar por Mes
                dict(label="Mes",
                     method="update",
                     args=[{"x": [df_month['Month'], df_month['Month']],
                            "y": [df_month['Utilidad Bruta'], df_month['Utilidad Neta']],
                            "type": "bar"},
                           {"title": "Comparación por Mes",
                            "xaxis": {"title": "Mes"},
                            "yaxis": {"title": "Utilidad"}}]),
                # Opción para agrupar por Día
                dict(label="Día",
                     method="update",
                     args=[{"x": [df_day['Day'], df_day['Day']],
                            "y": [df_day['Utilidad Bruta'], df_day['Utilidad Neta']],
                            "type": "bar"},
                           {"title": "Comparación por Día",
                            "xaxis": {"title": "Día"},
                            "yaxis": {"title": "Utilidad"}}])
            ]),
            direction="down",
            showactive=True,
        )
    ]
)

# Ajustar los títulos y modo de apilado
fig.update_layout(
    barmode='overlay',
    title='Comparación de Utilidad Bruta y Neta',
    xaxis_title='Fecha',
    yaxis_title='Utilidad'
)

df1 = pd.read_csv('Grafica4.csv')
import plotly.express as px  # Add this line at the top of your code

# Select only numeric columns for summing

numeric_columns = df1.select_dtypes(include=['float64', 'int64']).columns

# Group by 'Date' and sum only numeric columns
data_grouped = df1.groupby('Date')[numeric_columns].sum().reset_index()

# Line chart for revenue (Bike Rentals over time)
fig_revenue_cost = px.line(data_grouped, x='Date', y='Utilidad Neta', 
                        title="Utilidad Neta en el Tiempo", 
                        labels={'Net Income'})

df2 = pd.read_csv('Grafica5.csv')
# Exclude non-numeric columns when grouping and summing
numeric_columns = df2.select_dtypes(include=['float64', 'int64']).columns

# Group by month and sum only numeric columns
heatmap_data = df2.groupby('Seasons')[numeric_columns].sum().reset_index()

# Create the heatmap
heatmap_fig = px.density_heatmap(heatmap_data, x='Seasons', y='Utilidad Neta', 
                                title="Renta de Bicicletas Mensual vs Utilidad Neta (Estación)",
                                labels={'Rented Bike Count': 'Bike Rentals', 'Month': 'Month'})

# Layout de la página
app.layout = html.Div(children=[
    
    html.Img(src='/assets/REP.png', style={'width': '100%', 'height': 'auto'}),
    
    html.Div(id='head-image', children=[]),
    
    # Contenedor con los tres botones centrados
    html.Div([
        html.Button('Diario', id='button-1', n_clicks=0),
        html.Button('Mensual', id='button-2',  n_clicks=0, style={'marginLeft': '10px', 'marginRight': '10px'}),
        html.Button('Anual', id='button-3',  n_clicks=0)
    ], style={'textAlign': 'center', 'marginTop': '20px'}),

    # Espacio para mostrar la imagen seleccionada
    html.Div(id='image-output', children=[]),

    # División 1 con Título de segundo nivel
    html.Div(children=[
        html.H2('Influencia de las Estaciones sobre la Renta de Bicicletas', style={'color': 'white', 'backgroundColor': 'darkblue','textAlign': 'center'}),
        dcc.Graph(
        id='example-graph',
        figure=heatmap_fig
    ),
    ]),

    # División 2 con Título de segundo nivel
    html.Div(children=[
        html.H2('Rentabilidad Financiera en el Tiempo', style={'color': 'white', 'backgroundColor': 'darkblue','textAlign': 'center'}),
        dcc.Graph(
        id='example-graph',
        figure=fig
    ),
    ]),
    
    # División 3 con Título de segundo nivel
    html.Div(children=[
        html.H2('Prediccion de la Rentabilidad Financiera', style={'color': 'white', 'backgroundColor': 'darkblue','textAlign': 'center'}),
        dcc.Graph(
        id='example-graph',
        figure=fig_revenue_cost
    ),
    ]),
    
    # División 4 con Título de segundo nivel
    
    html.Div(children=[
        html.H2('Rentabilidad Financiera', style={'color': 'white', 'backgroundColor': 'darkblue','textAlign': 'center'}),
        html.Img(src='/assets/RENT.png', style={'width': '100%', 'height': 'auto'}),
    ]),

    # Pie de página
    html.Img(src='/assets/AS.png', style={'width': '100%', 'height': 'auto'}),
],
style={'backgroundColor': 'white', 'padding': '20px'})  # Fondo azul claro y padding


# Callback para actualizar la imagen basada en el botón seleccionado
@app.callback(
    Output('image-output', 'children'),
    [Input('button-1', 'n_clicks'), 
     Input('button-2', 'n_clicks'), 
     Input('button-3', 'n_clicks')],
    [State('button-1', 'n_clicks_timestamp'),
     State('button-2', 'n_clicks_timestamp'),
     State('button-3', 'n_clicks_timestamp')]
)
def display_output(n1, n2, n3, ts1, ts2, ts3):
    
    ts1 = ts1 or 0
    ts2 = ts2 or 0
    ts3 = ts3 or 0
    
    if ts1 is not None and (ts1 > ts2 or ts2 is None) and (ts1 > ts3 or ts3 is None):
        return html.Img(src='/assets/IMG_DIA.png', style={'width': '100%', 'margin': '20px auto'})
    elif ts2 is not None and (ts2 > ts1 or ts1 is None) and (ts2 > ts3 or ts3 is None):
        return html.Img(src='/assets/IMG_MEN.png', style={'width': '100%', 'margin': '20px auto'})
    elif ts3 is not None and (ts3 > ts1 or ts1 is None) and (ts3 > ts2 or ts2 is None):
        return html.Img(src='/assets/IMG_AN.png', style={'width': '100%', 'margin': '20px auto'})
    else:
        return html.P('Selecciona la temporalidad')
    
    
if __name__ == '__main__':
    app.run_server(debug=True)
