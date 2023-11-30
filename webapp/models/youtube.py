import googleapiclient.discovery
import json

config_data = open('config.json')
config = json.load(config_data)
config_data.close

api_key = config.get('youtube_api_key')


def get_comments(video_id):
    comments = []
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey = api_key)
    
    params = {        
        'part': 'snippet',
        'videoId': video_id,
        'textFormat': 'plainText',
        'maxResults': 100,
        # 'moderationStatus': 'published'
    }

    request = youtube.commentThreads().list(**params)
    response = request.execute()

    api_calls = 1
    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        if api_calls == 10:
            print("10 youtube api calls reached. Exiting loop")
            break

        if 'nextPageToken' in response:
            params['pageToken'] = response['nextPageToken']
            response = youtube.commentThreads().list(**params).execute()
            api_calls += 1
            print(params)
        else:
            break

    return comments


# print(get_comments('mzwE-8-L5YA'))

