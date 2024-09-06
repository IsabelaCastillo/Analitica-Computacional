import dash
from dash import dcc  # dash core components 
from dash import html # dash html components
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
print(df.columns)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df_grouped = df.groupby(['year', 'continent'])['lifeExp'].mean().reset_index()

# Crear el gráfico de líneas
fig2 = px.line(df_grouped, x="year", y="lifeExp", color="continent",
              title='Evolución del Promedio de Esperanza de Vida por Continente',
              labels={'lifeExp': 'Esperanza de Vida Promedio'})


app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    ),
    dcc.Graph(
        id='graph2',
        figure=fig2
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp", 
                     size="pop", color="continent", hover_name="country", 
                     log_x=True, size_max=55,
                     labels={
                     "pop": "Population",
                     "gdpPercap": "GDP per cápita",
                     "lifeExp": "Life Expectancy",
                     "continent": "Continent"
                     },
                     title="Life expectancy vs. GDP per cápita across the years")

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
