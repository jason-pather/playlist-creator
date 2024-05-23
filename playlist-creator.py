import json
import argparse
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

# Function to convert timestamp to datetime object
def timestamp_to_datetime(timestamp_ms):
    return datetime.fromtimestamp(timestamp_ms / 1000.0)

# Function to extract Spotify links within a date range
def extract_spotify_links(json_data, start_date, end_date, spotify):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    spotify_links = []
    
    for message in json_data['messages']:
        message_time = timestamp_to_datetime(message['timestamp_ms'])
        
        if start_date <= message_time <= end_date:
            if 'share' in message and 'link' in message['share']:
                link = message['share']['link']
                if link.startswith("https://open.spotify.com/track/"):
                    spotify_links.append({
                        "link": link,
                        "timestamp": message_time,
                        "sender": message['sender_name']
                    })
                elif link.startswith("https://open.spotify.com/album/"):
                    most_played_track = get_most_played_track_from_album(link, spotify)
                    if most_played_track:
                        spotify_links.append({
                            "link": most_played_track,
                            "timestamp": message_time,
                            "sender": message['sender_name']
                        })
    
    return spotify_links

# Function to get the most played track from an album
def get_most_played_track_from_album(album_url, spotify):
    try:
        album_id = album_url.split("/")[-1].split("?")[0]
        tracks = spotify.album_tracks(album_id)
        track_popularity = [
            (track['popularity'], track['external_urls']['spotify'])
            for track in tracks['items']
            if 'popularity' in track and 'external_urls' in track and 'spotify' in track['external_urls']
        ]
        if track_popularity:
            most_played_track = max(track_popularity, key=lambda x: x[0])
            return most_played_track[1]
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching album tracks for album ID {album_id}: {e}")
    return None

# Function to create a new Spotify playlist and add tracks to it
def create_spotify_playlist(spotify, playlist_name, spotify_links):
    print(spotify.me())
    user_id = spotify.me()['id']
    playlist = spotify.user_playlist_create(user_id, playlist_name, public=False)
    playlist_id = playlist['id']
    
    # Extract track URIs from spotify_links
    track_uris = [link['link'] for link in spotify_links]
    
    # Add track URIs to the playlist
    spotify.playlist_add_items(playlist_id, track_uris)
    
    return playlist_id

# Main function to parse arguments and call the extraction function
def main():
    parser = argparse.ArgumentParser(description="Extract Spotify links from JSON messages within a date range.")
    parser.add_argument('json_file', type=str, help='Path to the JSON file containing messages')
    parser.add_argument('start_date', type=str, help='Start date in YYYY-MM-DD format')
    parser.add_argument('end_date', type=str, help='End date in YYYY-MM-DD format')
    parser.add_argument('playlist_name', type=str, help='Name for the new playlist')
    
    args = parser.parse_args()

    with open(args.json_file, 'r') as file:
        json_data = json.load(file)

    with open('config.json', 'r') as config_file:
        config_data = json.load(config_file)
        client_id = config_data['client_id']
        client_secret = config_data['client_secret']
    
    # Authenticate with Spotify API
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    token = util.prompt_for_user_token('jasonpather', scope="playlist-modify-private playlist-read-private playlist-modify-public")
    spotify = spotipy.Spotify(auth_manager=auth_manager, auth=token)

    spotify_links = extract_spotify_links(json_data, args.start_date, args.end_date, spotify)

    if not spotify_links:
        print("No Spotify links found in the specified date range.")
    else:
        for link_info in spotify_links:
            print(f"Link: {link_info['link']}, Timestamp: {link_info['timestamp']}, Sender: {link_info['sender']}")
        
        playlist_id = create_spotify_playlist(spotify, args.playlist_name, spotify_links)
        print(f"Playlist created successfully! Playlist ID: {playlist_id}")
            
if __name__ == "__main__":
    main()
