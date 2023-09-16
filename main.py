from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
import os
import requests
import spotipy

URL = "https://www.billboard.com/charts/hot-100/"
date = input("Find the trending of the week on billboard! Type the date in this format YYYY-MM-DD: ")


response = requests.get(URL + date)
soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]
top_10_songs = song_names[:10]


# Spotify API authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:3000/",
        client_id= os.environ.get('SPOTIFY_CLIENT_ID'),
        client_secret= os.environ.get('SPOTIFY_CLIENT_SECRET'),
        show_dialog=True,
        cache_path="token.txt",
        username="Pan", 
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in top_10_songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(json.dumps(result, sort_keys=4, indent=4))
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

# Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

