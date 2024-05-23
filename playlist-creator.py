import json
import argparse
from datetime import datetime

# Function to convert timestamp to datetime object
def timestamp_to_datetime(timestamp_ms):
    return datetime.fromtimestamp(timestamp_ms / 1000.0)

# Function to extract Spotify links within a date range
def extract_spotify_links(json_data, start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    
    spotify_links = []
    
    for message in json_data['messages']:
        message_time = timestamp_to_datetime(message['timestamp_ms'])
        print(f"Checking message at {message_time}")  # Debugging line

        if start_date <= message_time <= end_date:
            print(f"Message in range: {message}")  # Debugging line
            if 'share' in message and 'link' in message['share']:
                link = message['share']['link']
                if "open.spotify.com" in link:
                    print(f"Spotify link found: {link}")  # Debugging line
                    spotify_links.append({
                        "link": link,
                        "timestamp": message_time,
                        "sender": message['sender_name']
                    })
    
    return spotify_links

# Main function to parse arguments and call the extraction function
def main():
    parser = argparse.ArgumentParser(description="Extract Spotify links from JSON messages within a date range.")
    parser.add_argument('json_file', type=str, help='Path to the JSON file containing messages')
    parser.add_argument('start_date', type=str, help='Start date in YYYY-MM-DD format')
    parser.add_argument('end_date', type=str, help='End date in YYYY-MM-DD format')
    
    args = parser.parse_args()

    with open(args.json_file, 'r') as file:
        json_data = json.load(file)

    spotify_links = extract_spotify_links(json_data, args.start_date, args.end_date)

    if not spotify_links:
        print("No Spotify links found in the specified date range.")
    else:
        for link_info in spotify_links:
            print(f"Link: {link_info['link']}, Timestamp: {link_info['timestamp']}, Sender: {link_info['sender']}")

if __name__ == "__main__":
    main()
