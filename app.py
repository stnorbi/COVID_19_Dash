
from __future__ import print_function
from httplib2 import Http
import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import dash_table
import plotly.graph_objs as go
import plotly

#own moduls
import scraper as src
import detail_scraper as d_src

main_df=src.main('Hungary')


details=d_src.detail_table()
distgend=d_src.dist_gend(details)
avg_man, avg_wmn=d_src.avg_ages(details)
distage=d_src.dist_age(details)



app = dash.Dash(__name__)
server = app.server


app.layout = html.Div([
        html.H1('COVID-19 DASHBOARD MAGYARORSZÁG'),
        dcc.Graph(
                id='active',
                figure={
                    'data': [go.Line(
                            x = main_df.index,
                            y = main_df['Aktív'],
                            )
                    ],
                    'layout': go.Layout(
                        legend={'x': 0, 'y': 1},
                        hovermode='closest',
                        title='Aktív fertőzöttek száma',
                    )
                }
        ),
        dcc.Graph(
        id='cases',
        figure={
            'data': [go.Line(
                    x = main_df.index,
                    y = main_df['Eset'],
                    )
            ],
            'layout': go.Layout(
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                title='Esetek száma',
                    )
               }
        ),
        dcc.Graph(
        id='casedeathD',
        figure={
            'data': [go.Bar(
                    x = main_df.index,
                    y = main_df['EsetD'],
                    )
            ],
            'layout': go.Layout(
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                title='Esetek változása (előző naphoz képest)',
                    )
               }
        ),
        dcc.Graph(
        id='deathbar',
        figure={
            'data': [go.Bar(
                    x = main_df.index,
                    y = main_df['HalottD'],
                    )
            ],
            'layout': go.Layout(
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                title='Halálozások változása (előző naphoz képest)',
                    )
               }
        ),
])

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})



if __name__ == '__main__':
    app.run_server(debug=True)