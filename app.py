# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

df = pd.read_csv('data/data.csv')

df = df.groupby(['genre', 'year'], as_index = False).mean()
colors = ["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6", "#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99", "#aaaa11", "#6633cc", "#e67300", '#000000']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(
        id='music-trends',
        figure={
            'data': [
                dict(
                    x=df[df['genre'] == genre]['year'],
                    y=df[df['genre'] == genre]['num_words'],
                    opacity=0.7,
                    mode='lines',
                    marker=dict(color = colors[i]),
                    name=genre
                ) for i, genre in enumerate(df.genre.unique())
            ],
            'layout': dict(
                xaxis={'title': 'Year'},
                yaxis={'title': 'Number of Words'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                line={'shape': 'spline', 'smoothing': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
