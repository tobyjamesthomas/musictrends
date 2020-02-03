import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = 'Music Trends'

server = app.server # Flask

songs = pd.read_csv('data/data.csv')

df = songs.groupby(['genre', 'year'], as_index = False).mean()

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

colors = {
    'alternative/indie': '#3366cc',
    'blues': '#dc3912',
    'classical/soundtrack': '#ff9900',
    'country': '#109618',
    'disco': '#990099',
    'electronic/dance': '#0099c6',
    'folk': '#dd4477',
    'hip-hop/rnb': '#66aa00',
    'jazz': '#b82e2e',
    'pop': '#316395',
    'reggae': '#994499',
    'religious': '#22aa99',
    'rock': '#aaaa11',
    'soul': '#6633cc',
    'swing': '#e67300',
    'none': '#cccccc'
}

app.layout = html.Div([

    html.H1('Music Trends in the Billboard Top 100 Songs'),

    html.Div([
        html.Div([
            html.A('About this data', className='button', href='#about'),
        ], className='interior'),
    ], className='modal-button'),

    html.Label('Genres'),
    dcc.Dropdown(
        id='genres',
        options=[{'label': i, 'value': i} for i in df.genre.unique()],
        value=[i for i in df.genre.unique()],
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

    dcc.Graph(id='music-billboard'),

    html.Div([
        html.P('Made with 💙for Apple'),
    ], className='footer'),

    html.Div([
        html.Div([
            html.A('Close', className='modal-close', title='close', href='#'),
            html.H1('Data'),
            html.P('''
                This dataset originates from the Billboard\'s Top 100 songs over the years 1950-2015.
            '''),
        ]),
    ], id='about', className='modal-window'),
])

@app.callback(
    Output('music-trends', 'figure'),
    [Input('genres', 'value'),
    Input('measurement', 'value'),
    Input('year-slider', 'value')])
def update_graph(genres, measurement, year_range):

    dff = df
    data = []
    years = [i for i in range(year_range[0], year_range[1]+1)]
    for genre in genres:
        tracks = df[(df['genre'] == genre) & df['year'].isin(years)]

        data.append(dict(
            x = tracks['year'],
            y = tracks[measurement],
            opacity = 0.7,
            marker = {'color': colors[genre]},
            name = genre
        ))

    return {
        'data': data,
        'layout': dict(
            xaxis={'title': 'Year'},
            yaxis={'title': measurements[measurement]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            hovermode='closest'
        )
    }

@app.callback(
    Output('music-billboard', 'figure'),
    [Input('genres', 'value'),
    Input('year-slider', 'value')])
def update_graph(genres, year_range):

    df = songs
    data = []
    years = [i for i in range(year_range[0], year_range[1]+1)]
    for genre in genres:
        tracks = df[(df['genre'] == genre) & df['year'].isin(years)]

        text = tracks['title'] + ' by ' + tracks['artist']

        data.append(dict(
            x = tracks['year'],
            y = tracks['pos'],
            text = text,
            mode = 'markers',
            opacity = 0.7,
            marker = {
                'size': 10,
                'color': colors[genre],
            },
            name = genre
        ))

    return {
        'data': data,
        'layout': dict(
            xaxis={'title': 'Year'},
            yaxis={'title': 'Billboard Position', 'autorange': 'reversed'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug = True)
