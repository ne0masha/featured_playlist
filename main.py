from dotenv import load_dotenv
import os
from yandex_music import Client
import re

load_dotenv()


def is_latin(text):
    return bool(re.match('^[a-zA-Z]+$', text))

MY_TOKEN_YM = os.environ.get('TOKEN_YM')
client = Client(MY_TOKEN_YM).init()

liked_list = client.users_likes_tracks().fetch_tracks()

tracks = []

for item in liked_list:

    track_info = {
        'title': item['title'],
        'artist': item['artists'][0]['name'],
        'likes_count': item['albums'][0]['likes_count']
    }
    tracks.append(track_info)


tracks.sort(key=lambda x: x['likes_count'], reverse = True)

top_tracks = []
count = 0

for track in tracks:
    if is_latin(track['title']) and is_latin(track['artist']):
        top_tracks.append(track)
        count += 1

    if count == 5: break


#------------------------------------Writing to file-------------------------------------

with open("output.txt", "w") as file:
    file.write('TOP-5 MOST LIKED NOT RUSSIAN TRACKS FROM YANDEX MUSIC FROM YOUR LIKED PLAYLIST:\n\n')

    for track in top_tracks:
        file.write(f"{track['title']} - {track['artist']} ({track['likes_count']} likes)\n")

file.close()