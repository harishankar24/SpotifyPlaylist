
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from confidential_data import client_id, client_secret
# from os import system
# system('cls')

REDIRECT_URI = "https://spotifydemo.com"
TOP = 10

#1. Pick a date
picked_date = input("Enter a date in 'YYYY-MM-DD' format: ?\b")
# picked_date = "2000-08-12"

#2. Scrap TOP 'X' songs of that particular day
URL = "https://www.billboard.com/charts/hot-100/"

response = requests.get(url = f"{URL}{picked_date}")
billboard_webpage_html = response.text
soup = BeautifulSoup(billboard_webpage_html,"html.parser")
all_songs = soup.find_all(name = "span", class_ = "chart-element__information__song")
top_100_songs = []
for i in range(TOP):
  top_100_songs.append(all_songs[i].text)

#3. Authenticate yourself on Spotify
sp = spotipy.Spotify(
    auth_manager = SpotifyOAuth(
        scope = "playlist-modify-private",
        redirect_uri = REDIRECT_URI,
        client_id = client_id,
        client_secret = client_secret,
        show_dialog = True,
        cache_path = "token.txt"
    )
)
user_id = sp.current_user()["id"]

#4. Get URI of all the songs that are available on Spotify. Skip others.
song_uris = []
year = picked_date.split('-')[0]
for song in top_100_songs:
  result = sp.search(q = f"track:{song} year:{year}", type = "track")
  # print(result)
  try:
    uri = result["tracks"]["items"][0]["uri"]
    song_uris.append(uri)
  except IndexError:
        print(f"{song} <- doesn't exist in Spotify. Skipped.")

#5. Create a playlist on Spotify
playlist = sp.user_playlist_create(user = user_id, name = f"{picked_date} Billboard 100", public = False)

#6. Add the songs's uri to the created playlist
sp.playlist_add_items(playlist_id = playlist["id"], items = song_uris)
