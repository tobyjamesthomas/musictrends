import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collections import defaultdict

client_credentials_manager = SpotifyClientCredentials(
    client_id="3f0028fc55bd49a3b849878769d8f1d4",
    client_secret="704b7b3da68248439a49c70d1dc34a3a"
)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

df = pd.read_json('raw/data.json')

def get_audio_features(title, artist):
    print("Searching Spotify for", title, "by", artist)

    songs = sp.search(
        q='track:' + title + ' artist:' + artist + '*',
        type='track'
    )

    items = songs['tracks']['items']

    if len(items) > 0:
        print("Getting audio features")

        song_id = str(items[0]['id'])
        features = sp.audio_features(song_id)[0]

        if len(features) >= 18:
            return features

    print("None found")

    return defaultdict(lambda: None)


def aggregate_data():
    output = pd.DataFrame()

    for i in range(0, len(df)):
        year_hits = pd.DataFrame(df.iloc[i]['songs'])
        size = len(year_hits)

        neg = [None] * size
        neu = [None] * size
        pos = [None] * size
        compound = [None] * size
        genre = [None] * size
        danceability = [None] * size
        energy = [None] * size
        loudness = [None] * size
        instrumentalness = [None] * size
        liveness = [None] * size
        spotify_id = [None] * size
        spotify_url = [None] * size
        duration_ms = [None] * size

        for j in range(0, size):
            track = year_hits.iloc[j]

            neg[j] = track.sentiment['neg']
            neu[j] = track.sentiment['neu']
            pos[j] = track.sentiment['pos']
            compound[j] = track.sentiment['compound']

            tags = track.tags
            genre[j] = tags[0] if tags else 'none'

            audio_features = get_audio_features(track.title, track.artist)
            danceability[j] = audio_features['danceability']
            energy[j] = audio_features['energy']
            loudness[j] = audio_features['loudness']
            instrumentalness[j] = audio_features['instrumentalness']
            liveness[j] = audio_features['liveness']
            spotify_id[j] = audio_features['id']
            spotify_url[j] = audio_features['track_href']
            duration_ms[j] = audio_features['duration_ms']

        year_hits['sentiment_neg'] = neg
        year_hits['sentiment_neu'] = neu
        year_hits['sentiment_pos'] = pos
        year_hits['sentiment_compound'] = compound
        year_hits['genre'] = genre
        year_hits['danceability'] = danceability
        year_hits['energy'] = energy
        year_hits['loudness'] = loudness
        year_hits['instrumentalness'] = instrumentalness
        year_hits['liveness'] = liveness
        year_hits['spotify_id'] = spotify_id
        year_hits['spotify_url'] = spotify_url
        year_hits['duration_ms'] = duration_ms

        path = r'year/' + str(df.iloc[i]['year']) + r'.csv'
        year_hits.to_csv(path)

        output = output.append(year_hits, ignore_index = True)

    output.to_csv('data.csv')

aggregate_data()
