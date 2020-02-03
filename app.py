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

playlist = pd.DataFrame();

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
            html.A('About this data', className='button', href='#about-modal'),
        ], className='modal-button'),
        
        html.Div([
            html.A('Generate playlist', className='button', href='#playlist-modal'),
        ], className='modal-button'),
    ], style = {'display': 'flex'}),

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
    ], id='about-modal', className='modal-window'),

    html.Div([
        html.Div([
            html.A('Close', className='modal-close', title='close', href='#'),
            html.Div(id = 'playlist'),
            html.Button('Add to Apple Music (Coming Soon)', className = 'add-to-button disabled'),
            html.Button('Add to Spotify', className = 'add-to-button', id = 'add-to-spotify', n_clicks = 0),
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
    Output(component_id='playlist', component_property='children'),
    [Input('genres', 'value'),
    Input('year-slider', 'value')])
def update_playlist(genres, year_range):
    if len(genres) < 1:
        return html.P('Please select a genre.')

    years = [i for i in range(year_range[0], year_range[1]+1)]

    playlist = songs[songs[
        'genre'].isin(genres)
        & songs['year'].isin(years)
        & songs['spotify_url']]

    playlist = playlist.sample(min(len(playlist), 10))

    if len(playlist) < 1:
        return html.P('Please widen your selection.')

    song_list = [html.P(
        "{} by {}".format(song['title'], song['artist'])
    ) for i, song in playlist.iterrows()]

    return [
        html.H1("We sampled {} songs from your selection:".format(len(playlist)))
    ] + song_list

@app.callback(
    Output(component_id='add-to-spotify', component_property='children'),
    [Input('add-to-spotify', 'n_clicks')])
def update_spotify(n_clicks):
    return 'Added to Spotify' if n_clicks > 0 else 'Add to Spotify'

if __name__ == '__main__':
    app.run_server(debug = True)
