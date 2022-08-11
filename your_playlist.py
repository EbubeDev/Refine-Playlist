import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

date_search = input("What year would you like to travel to? Type date in this format YYYY-MM-DD: ")

BILL_URL = f"https://www.billboard.com/charts/hot-100/{date_search}/"

OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"
sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:8888/callback",
        client_id="*************************",
        client_secret="*******************",
        show_dialog=True,
        cache_path="token.txt")
)

user_id = sp.current_user()["id"]

response = requests.get(BILL_URL)
bill_html = response.text
egusi_soup = BeautifulSoup(bill_html, "html.parser")

top_100 = egusi_soup.select(selector="li #title-of-a-story")

song_titles = [song.getText().strip() for song in top_100]
song_uris = []
year = date_search.split("-")[0]

for song in song_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        pass

playlist = sp.user_playlist_create(user=user_id, name=f"{date_search} BILLBOARD TOP 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
