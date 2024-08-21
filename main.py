import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import tkinter

import requests
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont, ImageTk

scope = "user-library-read user-read-currently-playing user-read-playback-state user-modify-playback-state app-remote-control user-read-recently-played"

CLIENT_ID = ""
CLIENT_SECRET = ""

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://localhost:8888/callback"))

first = True
started = False
currently_playing = ""
large = True

def skip():
    sp.next_track()
def back():
    sp.previous_track()

def image(album, title, artist):
    if not large:
        if len(title) > 12:
            title = title[:11] + "..."
        if len(artist) > 23:
            artist = artist[:22] + "..."

        response = requests.get(album)
        cover = Image.open(BytesIO(response.content))
        cover = cover.resize((150,150), Image.LANCZOS)
        background = Image.open("background.jpeg")
        
        background.paste(cover, (20, 45))
        background.save("album_cover.jpg")
        img = Image.open("album_cover.jpg")
        
        draw = ImageDraw.Draw(img)
        draw.text((180, 45), title, fill=(179,179,179), font=ImageFont.truetype("circular.ttf", size=20))

        draw.text((180, 80), artist, fill=(83,83,83), font=ImageFont.truetype("circular.ttf", size=10))
        img.save("album_cover.jpg")
    else:
        if len(title) > 15:
            title = title[:14] + "..."
        if len(artist) > 30:
            artist = artist[:29] + "..."

        response = requests.get(album)
        cover = Image.open(BytesIO(response.content))
        cover = cover.resize((800,800), Image.LANCZOS)
        background = Image.open("background_large.jpeg")
        
        background.paste(cover, (140, 140))
        background.save("album_cover.jpg")
        img = Image.open("album_cover.jpg")
        
        draw = ImageDraw.Draw(img)
        draw.text((1100, 200), title, fill=(179,179,179), font=ImageFont.truetype("circular.ttf", size=90))

        draw.text((1100, 300), artist, fill=(83,83,83), font=ImageFont.truetype("circular.ttf", size=50))
        img.save("album_cover.jpg")


def update():
    global currently_playing
    results = sp.current_playback()
    currently_playing = results['item']['name']
    artist_name = results['item']['artists'][0]['name']
    print("Currently playing", results['item']['name'], "by", results['item']['artists'][0]['name'])
    album = results['item']['album']['images'][0]['url']
    image(album, currently_playing, artist_name)
    with open('index.html', 'w') as f:
        f.write(f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="refresh" content="2"> 
            <title>Spotify Currently Playing</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin-top: 50px;
                }}
            </style>
        </head>
        <body>
            <h1>Currently Playing</h1>
            <p>Song: {currently_playing}</p>
            <p>Artist: {artist_name}</p>
            <img src="album_cover.jpg" alt="Album">
        </body>
        </html>
        ''')

def empty():
    if not large:
        background = Image.open("background.jpeg")
        background.save("album_cover.jpg")
    else:
        background = Image.open("background_large.jpeg")
        background.save("album_cover.jpg")

    with open('index.html', 'w') as f:
        f.write(f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="refresh" content="2"> 
            <title>Spotify Currently Playing</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin-top: 50px;
                }}
            </style>
        </head>
        <body>
            <h1>Not Playing</h1>
            <img src="album_cover.jpg" alt="Album">
        </body>
        </html>
        ''')

while first:
    while not started:
        try:
            results = sp.current_playback()
            if results == None:
                print("Nothing is currently playing")
                empty()
                time.sleep(2)
            else:
                update()
                started = True
                first = False
        except:
            print("Nothing is currently playing")
            empty()
            time.sleep(2)


while started:
    try:
        
        results = sp.current_playback()
        try:
            if results['item']['name'] != currently_playing:
                update()
                time.sleep(2)
            elif results == None:
                print("Nothing is currently playing")
                empty()
                time.sleep(2)
            else:
                time.sleep(2)
        except TypeError:
            print("Nothing is currently playing")
            empty()
            time.sleep(2)

    except:
        print("Nothing is currently playing")
        empty()
        time.sleep(2)





