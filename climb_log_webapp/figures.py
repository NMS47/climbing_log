import pandas as pd
from dash import dcc, html, Input, Output

from django_plotly_dash import DjangoDash

class my_dash_plot(DjangoDash):

    def __init__(self, df):
        self.df = df
    

    app = DjangoDash('climb_stats')   # replaces dash.Dash
    df = pd.DataFrame(df)
    n_df = df.groupby('date_of_climb').value_counts().reset_index().rename(columns={0:'num_climbs'})
    print(n_df)

    app.layout = html.Div([
        html.H2("Estadisticas de escalada:", style={'text-align':'center'}),
        dcc.Dropdown(
            id='select_style',
            options=[{'label': 'Boulder', 'value': 'boulder'},
                        {'label': 'Deportiva', 'value': 'sport'},
                        {'label': 'Trad', 'value': 'trad'}],
            value='boulder',
            style={'width':'40%'},
        ),
        html.Div(id='output-container', children=[]),
        html.Br(),
        dcc.Graph(id='climbing_stats', figure={}),
    ],
    style={'height':'500px'},
    )

    @app.callback(
        #interntar devolviendo solo el ouput de figure porque solo vatos a devolver una cosa
        [Output(component_id='output-container', component_property='children'),
        Output(component_id='climbing_stats', component_property='figure')],
        [Input(component_id='select_style', component_property='value')]
    )
    def update__line_chart(style_selected):
        print(style_selected)
        container = 'Esto hay que borrarlo'

        dff = n_df['date_of_climb', 'climb_style', 'num_climbs']
        dff = dff [dff('climb_style') == style_selected ]
        print(dff)
        fig = px.line(dff, 
                x="date_of_climb", y="num_climbs", color="climb_style")
        return container, fig