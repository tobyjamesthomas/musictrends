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
    'pos': 'Billboard position',
    'duration_ms': 'Duration (ms)',
    'num_words': 'Number of words',
    'num_syllables': 'Number of syllables',
    'num_lines': 'Number of lines',
    'num_dupes': 'Number of duplicate lines',
    'difficult_words': 'Number of difficult words',
    'flesch_index': 'Flesch readability index (100 = Pre-K, 0 = Impossible)',
    'f_k_grade': 'Flesch-Kincaid readability index (Grade level required to read lyrics)',
    'fog_index': 'Gunning-Fog readability index (Grade level required to read lyrics)',
    'sentiment_pos': 'Positive sentiment (How happy the lyrics are)',
    'sentiment_neu': 'Neutral sentiment',
    'sentiment_neg': 'Negative sentiment (How sad the lyrics are)',
    'sentiment_compound': 'Sentiment (Compound)',
    'danceability': 'Danceability',
    'energy': 'Energy',
    'loudness': 'Loudness',
    'instrumentalness': 'Instrumentalness',
    'liveness': 'Liveness',
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
            html.A('About this dataset', className='button', href='#about-modal'),
        ], className='modal-button'),
        
        html.Div([
            html.A('Generate a playlist', className='button', href='#playlist-modal'),
        ], className='modal-button'),
    ], style = {'display': 'flex'}),

    html.Label('Genres'),
    dcc.Dropdown(
        id='genres',
        options=[{'label': i, 'value': i} for i in df.genre.unique()],
        value=[i for i in df.genre.unique()],
        multi=True,
    ),

    html.Label('Measurement (for the average song in that year and genre)'),
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
        value=[1970, 1990],
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
            html.P([
                'This dataset comes from ',
                html.A('Billboard', href = 'https://github.com/kevinschaich/billboard/tree/master/data'),
                '''
                and explores how music popular has evolved over the past few decades
                by analyzing the lyrics and musical composition of the Billboard's Top 100 songs
                over the years 1950-2015.
                ''',
            ]),
            html.P([
                'Further analysis has been made using ',
                html.A('Spotify API', href = 'https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/'),
                ' to add metrics such as song duration, instrumentalness and danceability.',
            ]),
            html.P([
                'This project was created by ',
                html.A('Toby Thomas', href = 'https://github.com/tobyjamesthomas'),
                ' and is built with ',
                html.A('Python', href = 'https://www.python.org/'),
                ', ',
                html.A('pandas', href = 'https://pandas.pydata.org/'),
                ', ',
                html.A('Flask', href = 'https://www.fullstackpython.com/flask.html'),
                ' and ',
                html.A('Plot.ly', href = 'https://plot.ly/'),
                '.',
            ]),
        ]),
    ], id='about-modal', className='modal-window'),

    html.Div([
        html.Div([
            html.A('Close', className='modal-close', title='close', href='#'),
            html.Div(id = 'playlist'),
            html.Div([
                html.Button('Reshuffle', className = 'add-to-button', id = 'reshuffle', n_clicks = 0),
                html.Button('Add to Apple Music (Coming Soon)', className = 'add-to-button disabled'),
                html.Button('Add to Spotify (Coming Soon)', className = 'add-to-button disabled'),
            ], id = 'export-buttons')
        ]),
    ], id='playlist-modal', className='modal-window'),
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

@app.callback(
    [Output(component_id='playlist', component_property='children'),
    Output(component_id='export-buttons', component_property='className')],
    [Input('genres', 'value'),
    Input('year-slider', 'value'),
    Input('reshuffle', 'n_clicks')])
def update_playlist(genres, year_range, n_clicks):
    if len(genres) < 1:
        return html.P('Please select a genre.'), 'hidden'

    years = [i for i in range(year_range[0], year_range[1]+1)]

    playlist = songs[songs[
        'genre'].isin(genres)
        & songs['year'].isin(years)
        & songs['spotify_url']]
    playlist = playlist.sample(min(len(playlist), 10))

    if len(playlist) < 1:
        return html.P('Please widen your selection.'), 'hidden'

    song_list = [html.P(
        "{} by {}".format(song['title'], song['artist'])
    ) for i, song in playlist.iterrows()]

    return (
        [html.H1("We sampled {} songs from your selection:".format(len(playlist)))
        ] + song_list,
        ''
    )


if __name__ == '__main__':
    app.run_server(debug = True)
