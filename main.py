import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

CLIENT_ID = "6d6ba3a71e79434ebf5b6f8d48feb4b2"
CLIENT_SECRET = "db18125fa8ee4d24b5b34b1a18b4dab4"


print("Welcome to the Music Time Machine!")
date = input("Enter the date you want to travel to (YYYY-MM-DD): ")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(URL)
billboard_data = response.text
soup = BeautifulSoup(billboard_data, "html.parser")
songs = soup.find_all(name="h3", id="title-of-a-story", class_="u-line-height-125")
song_titles = [title.getText().strip("\n\t") for title in songs]
artists = soup.find_all(name="span", class_="u-max-width-330")
artist_names = [name.getText().strip("\n\t") for name in artists]
song_and_artist = dict(zip(song_titles, artist_names))

print(song_and_artist)
print()
print("Searching for songs on Spotify and creating new playlist...")

sp = spotipy.Spotify(
     auth_manager=SpotifyOAuth(
         scope="playlist-modify-private",
         redirect_uri="http://example.com",
         client_id=CLIENT_ID,
         client_secret=CLIENT_SECRET,
         show_dialog=True,
         cache_path="token.txt"
     )
 )
user_id = sp.current_user()["id"]
print(user_id)

song_uris = []
for (song, artist) in song_and_artist.items():
    try:
        result = sp.search(q=f"track:{song} artist:{artist}", type="track")
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except:
         pass

print(f"Number of songs found: {len(song_uris)}")


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False, )

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print(f"New playlist '{date} Billboard 100' successfully created on Spotify!")
# response = requests.get(URL)
# web_page = response.text
# soup = BeautifulSoup(web_page, "html.parser")
#
# top_all_songs = soup.find_all(name="h3",id="title-of-a-story")
# print(top_all_songs)
# # top_songs = [song.getText() for song in top_all_songs]
#
#
# sp = spotipy.Spotify(
#     auth_manager=SpotifyOAuth(
#         scope="playlist-modify-private",
#         redirect_uri="http://example.com",
#         client_id=CLIENT_ID,
#         client_secret=CLIENT_SECRET,
#         show_dialog=True,
#         cache_path="token.txt"
#     )
# )
# user_id = sp.current_user()["id"]
# print(user_id)
#
# date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
# song_names = ["The list of song", "titles from your", "web scrape"]
#
# song_uris = []
# year = date.split("-")[0]
# for song in song_names:
#     result = sp.search(q=f"track:{song} year:{year}", type="track")
#     print(result)
#     try:
#         uri = result["tracks"]["items"][0]["uri"]
#         song_uris.append(uri)
#     except IndexError:
#         print(f"{song} doesn't exist in Spotify. Skipped.")
