from googleapiclient.discovery import build
import re
from pprint import pprint
# Set your API key
API_KEY = 'AIzaSyBVByj7rSJCak9gdzJBqNMS-tJUHY3dXxs'

# Create a service object for interacting with the YouTube API
youtube = build('youtube', 'v3', developerKey=API_KEY)

def youtube_search(search: str = 'tamil throwback songs'):
    # Example: Search for music videos
    search_query = search
    search_response = youtube.search().list(
        q=search_query,
        type='video',
        part='id,snippet',
        maxResults=10
    ).execute()
    return search_response

def find_video(video_id: str):

    # Request video details using the video ID
    video_response = youtube.videos().list(
        part='snippet,contentDetails,statistics',
        id=video_id
    ).execute()

    # Extract information from the response
    video_info = video_response['items'][0] if 'items' in video_response else None
    # pprint(video_info)
    return video_info

def is_duration_greater_than_10_minutes(duration):
    # Regular expression to extract hours, minutes, and seconds
    match = re.match(r'(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    if match:
        # Extract hours, minutes, and seconds from the match
        hours, minutes, seconds = map(lambda x: int(x) if x else 0, match.groups())
        # Convert everything to seconds and check if greater than 10 minutes
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return total_seconds > 600  # 10 minutes in seconds
    return False

def song_from_description(description: str, pattern: str = r'\d+:\d+\s(.*)'):
    songs = []
    # description = description.split("\n")
    stripped_description = [line.strip() for line in description.splitlines() if line.strip()]
    for line in stripped_description:
        match = re.search(pattern, line)
        if match:
            songs.append(match.group(1).strip())

    if len(songs) <2:
        songs = song_from_description(description, r'\d+\.\s(.*?)(?=\d+\:|\-|$)')

    return songs


def video_info_sort(video_info: dict):
    if video_info:
        snippet = video_info['snippet']
        content_details = video_info['contentDetails']

        # print(f"Video Title: {snippet['title']}")
        # print(f"Description: {snippet['description']}")
        # print(f"Duration: {content_details['duration']}")
        duration = content_details['duration'][2:]
        if is_duration_greater_than_10_minutes(duration):
            # go throguh description and find songs
            print("song over 10mins")
            print(snippet['description'])
            return song_from_description(snippet['description'])
        else:
            # get song from title and move on 
            song_title = snippet['title'].split('|')
            print(song_title[0])
            return song_title[0]

def returned_search(search_response: dict):
    # Example: Retrieve details about the videos
    songs_found = 0
    song_list = []
    for video in search_response['items']:
        print("extracting data")
        print(video)
        video_id = video['id']['videoId']
        video_title = video['snippet']['title']
        video_description = video['snippet']['description']
        print(f"Video ID: {video_id}\nTitle: {video_title}\nDescription: {video_description}\n")
        video_info = find_video(video_id)
        returned_song = video_info_sort(video_info)
        if songs_found >10:
            print("song list over 10")
            return song_list
        if isinstance(returned_song, list):
            if len(returned_song)>1:
                songs_found += len(returned_song)
                song_list.extend(returned_song)
        else:
            songs_found +=1
            print("appending")
            song_list.append(returned_song)
    return song_list

if __name__ =="__main__":
    response = {}
    search_response = youtube_search("tamil song")
    # search_response = youtube_search("VdDS7XDIsZg")
    # search_response = youtube_search()
    list_of_songs_to_add = returned_search(search_response)
    print(list_of_songs_to_add)
# search for something, find videos and for first 10 go to video, if length over x then go description and find songs, 
#                                                                   add to list 
