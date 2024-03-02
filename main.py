import requests
from dotenv import load_dotenv
import os
from yandex_music import Client
import re

#-----------------------------------VK------------------------------------------

load_dotenv()

MY_TOKEN_VK = os.getenv('TOKEN_VK')
MY_URL_VK = os.getenv('URL_VK')
version = 5.199

params = {
    'access_token': MY_TOKEN_VK,
    'fields': 'about, bdate, city, country, status, education',
    'v': version,
}

response = requests.get(MY_URL_VK, params)

df = response.json()['response'][0]

#-----------------------------------Yandex Music------------------------------------------

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
    file.write(

        'GENERAL INFORMATION FROM VK:\n\n' +
        'id: ' + str(df['id']) + '\n' +
        'Name: ' + str(df[u'first_name']) + ' ' + str(df[u'last_name']) + '\n' +
        'Status: ' + str(df['status']) + '\n' +
        'Birthdate: ' + str(df['bdate']) + '\n' +
        'Country, city: ' + str(df['country']['title']) + ', ' + str(df['city']['title']) + '\n' +
        'Education: ' + str(df['university_name']) + ' (' + str(df['faculty_name']) + ')' + '\n\n\n'
    )

file.close()

with open("output.txt", "a") as file1:
    file1.write('TOP-5 MOST LIKED NOT RUSSIAN TRACKS FROM YANDEX MUSIC FROM YOUR LIKED PLAYLIST:\n\n')

    for track in top_tracks:
        file1.write(f"{track['title']} - {track['artist']} ({track['likes_count']} likes)\n")

file1.close()