# playlist-creator

This script will extract Spotify links from a downloaded Messenger chat over a given date range, create a playlist in the user's account, add tracks from track links to the playlist, and add the most played track from album links to the playlist.

It requires a json file of the Messenger chay which can be downloaded here:
https://www.facebook.com/help/messenger-app/677912386869109

Requires Spotipy library - https://spotipy.readthedocs.io/en/2.22.1/

`pip install spotipy`

Requires the following auth scopes to be granted by the user's Spotify account: 
- `playlist-modify-private`
- `playlist-read-private`
- `playlist-modify-public`

Command to run script: `python3 [script filename] [Messenger json filename] [from date] [to date] [new playlist name]`

Example command: `python3 playlist-creator.py messages.json 2024-01-01 2024-01-31 "Metal Yarns January 2024"`
