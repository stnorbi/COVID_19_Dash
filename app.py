
from __future__ import print_function
from httplib2 import Http
import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import dash_bootstrap_components as dbc
import dash_table
import plotly.graph_objs as go
import plotly
from wordcloud import WordCloud
from io import BytesIO
import base64
from datetime import datetime as dtm


#own moduls
import scraper as src
import detail_scraper as d_src

#scraping and calculation
main_df=src.main('Hungary')


details=d_src.detail_table()
reason=details['Alapbetegségek'].values

distgend,nem=d_src.dist_gend(details)
avg_man, avg_wmn=d_src.avg_ages(details)
distage=d_src.dist_age(details)

#colors
colors = ['blue','red']



app = dash.Dash(external_stylesheets=[
    "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap-grid.min.css"
])
# app.scripts.append_script({
#     'external_url': '/static/ js/javascript.js?%s' % dtm.now(),
# })
server = app.server

#app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})


app.layout = html.Div([
        dbc.Row([html.H1('COVID-19 DASHBOARD MAGYARORSZÁG')], justify="center", align="center"),
        dbc.Row([
            dbc.Col(
                html.Div(
                dcc.Graph(id='g1',
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
                )
            ),width={'size':6}),            
            dbc.Col(html.Div(
                dcc.Graph(id='g2',
                    figure={
                    'data': [go.Line(
                            x = main_df.index,
                            y = main_df['Eset'],
                            name="Terjedés üteme"
                            ),
                            go.Line(
                             x=main_df.index,
                             y=main_df['Halott'],
                             name='Halott'
                            ),
                            go.Line(
                             x=main_df.index,
                             y=main_df['Gyógyult'],
                             name='Gyógyult'
                            )
                            ], 
                    'layout': go.Layout(
                            legend={'x': 0, 'y': 1},
                            hovermode='closest',
                            title='Esetek száma',
                            )
                    }
                )
            ),
            width={'size':6}),
        ]),
        dbc.Row([
            dbc.Col(html.Div(
                dcc.Graph(id='g3',
                    figure={
                    'data': [go.Bar(
                            x = main_df.index,
                            y = main_df['EsetD'],
                            )],
                    'layout': go.Layout(
                            legend={'x': 0, 'y': 1},
                            hovermode='closest',
                            title='Esetek változása (előző naphoz képest)',
                            )
                    }
                ),
            ),width={'size':6}),
            dbc.Col(html.Div(
                dcc.Graph(id='g4',
                    figure={
                        'data': [go.Bar(
                                x = main_df.index,
                                y = main_df['HalottD'],
                                )
                        ],
                        'layout': go.Layout(
                            legend={'x': 0, 'y': 1},
                            hovermode='closest',
                            title='Halál esetek száma (napi bontásban)',
                                )
                        }
                    ),
                ),width={'size':6}),
            ]),
        dbc.Row([
            dbc.Col(html.Div(
                dcc.Graph(id='g5',
                    figure={
                    'data': [go.Bar(
                            x=distgend.index,
                            y=distgend['Eset/Nem']
                            )],                    
                    'layout': go.Layout(
                            legend={'x': 0, 'y': 1},
                            hovermode='closest',
                            title='Halálozás megoszlása nemenként',
                            )
                        }
                    )
            )
            ,width={'size':6}),
            dbc.Col(
                html.Div(
                                dcc.Graph(id='g7',
                    figure={
                    'data': [go.Pie(
                            values=distage["Eset/Korcsoport"],
                            labels=distage.index
                            )
                            ],
                    'layout': go.Layout(
                            legend={'x': 0, 'y': 1},
                            hovermode='closest',
                            title='Halálesetek korszerinti megoszlása',
                            )
                    }
                )
            ),width={'size':6}),
            ]),
        html.Div(
            html.Div(
            [html.H3("Elhalálozottak átlag életkora nemenként"),
            html.P('Férfi: '+str(round(avg_man))+" év"),
            html.P('Nő: '+str(round(avg_wmn))+" év")
            ],style={'color': 'black', 'fontSize': 22}
            )
        ),
        dbc.Row([html.H2
        ('Elhunytak alapbetegségei')], justify="center", align="left"),
        dbc.Row([html.Img(id="image_wc")], justify="center", align="center"),
])







def get_wordcloud(data=None):
    text=str(data).replace('betegség','')
    text=text.replace('feltöltés alatt','')
    wc = WordCloud(background_color='black',
            width=800,
            height=400).generate(text)
    return wc.to_image()

@app.callback(Output('image_wc', 'src'), [Input('image_wc', 'id')])
def make_image(b):
    img = BytesIO()
    get_wordcloud(data=reason).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


if __name__ == '__main__':
    app.run_server(debug=True)