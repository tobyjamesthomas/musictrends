# -*- coding: utf-8 -*-
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('data/data.csv')
dfg = df.groupby(['genre', 'year'], as_index = False).mean()

measurements = {
    'num_lines': 'Number of lines',
    'f_k_grade': 'f_k_grade',
    'pos': 'pos',
    'num_syllables': 'num_syllables',
    'difficult_words': 'difficult_words',
    'fog_index': 'fog_index',
    'num_dupes': 'num_dupes',
    'flesch_index': 'flesch_index',
    'num_words': 'Number of words',
    'sentiment_neg': 'sentiment_neg',
    'sentiment_neu': 'sentiment_neu',
    'sentiment_pos': 'sentiment_pos',
    'sentiment_compound': 'sentiment_compound',
    'danceability': 'danceability',
    'energy': 'energy',
    'loudness': 'loudness',
    'instrumentalness': 'instrumentalness',
    'liveness': 'liveness',
    'duration_ms': 'Duration in miliseconds',
}

colors = [
    "#3366cc", "#dc3912", "#ff9900", "#109618",
    "#990099", "#0099c6", "#dd4477", "#66aa00",
    "#b82e2e", "#316395", "#994499", "#22aa99",
    "#aaaa11", "#6633cc", "#e67300", '#000000'
]

app.layout = html.Div([

    html.Label('Genres'),
    dcc.Dropdown(
        id='genres',
        options=[{'label': i, 'value': i} for i in dfg.genre.unique()],
        value=[i for i in dfg.genre.unique()],
        multi=True,
    ),

    html.Label('Measurement'),
    dcc.Dropdown(
        id='measurement',
        options=[{'value': v, 'label': l} for v, l in measurements.items()],
        value='num_words',
        clearable=False,
    ),

    dcc.Graph(id='music-trends'),

    dcc.RangeSlider(
        id='year-slider',
        min=1950,
        max=2015,
        marks={
            1950: '1950',
            1960: '1960',
            1970: '1970',
            1980: '1980',
            1990: '1990',
            2000: '2000',
            2010: '2010',
        },
        value=[1950, 2015],
        allowCross=False,
    ),
])

@app.callback(
    Output('music-trends', 'figure'),
    [Input('genres', 'value'),
    Input('measurement', 'value'),
    Input('year-slider', 'value')])
def update_graph(genres, measurement, year_range):

    years = [i for i in range(year_range[0], year_range[1]+1)]
    dff = dfg[dfg.genre.isin(genres) & dfg.year.isin(years)]

    return {
        'data': [
            dict(
                x=dff[dff['genre'] == genre]['year'],
                y=dff[dff['genre'] == genre][measurement],
                opacity=0.7,
                mode='lines',
                marker=dict(color = colors[i]),
                name=genre
            ) for i, genre in enumerate(genres)
        ],
        'layout': dict(
            xaxis={'title': 'Year'},
            yaxis={'title': measurements[measurement]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            line={'shape': 'spline', 'smoothing': 10},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug = True)
