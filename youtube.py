import os
import pandas as pd
from googleapiclient.discovery import build
from datetime import datetime


def get_top_videos(youtube, query, max_results):
    request = youtube.search().list(
        q=query,
        part='id,snippet',
        type='video',
        videoDefinition='high',
        videoDuration='any',
        maxResults=max_results,
        order='viewCount',
        regionCode='KR',
    )
    response = request.execute()
    
    video_ids = [item['id']['videoId'] for item in response['items']]
    video_details = youtube.videos().list(
        id=','.join(video_ids),
        part='snippet,statistics',
    ).execute()
    
    video_data = []

    for item in video_details['items']:
        title = item['snippet']['title']
        video_id = item['id']
        url = f'https://www.youtube.com/watch?v={video_id}'
        view_count = int(item['statistics']['viewCount'])
        like_count = item['statistics'].get('likeCount', 0)
        published_at = item['snippet']['publishedAt']
        channel_id = item['snippet']['channelId']
        thumbnail_url = item['snippet']['thumbnails']['default']['url']
        hashtags = ", ".join(item['snippet'].get('tags', []))
        channel_data = youtube.channels().list(
            id=channel_id,
            part='statistics',
        ).execute()
        subscriber_count = int(channel_data['items'][0]['statistics']['subscriberCount'])
        sub_growth_rate = (subscriber_count / (subscriber_count + view_count)) * 100

        video_data.append([title, url, view_count, like_count, published_at, channel_id, subscriber_count, sub_growth_rate, hashtags, thumbnail_url])
    
    return video_data

def save_to_file(video_data, query):
    columns = ['Title', 'URL', 'View Count', 'Like Count', 'Published At', 'Channel ID', 'Subscriber Count', 'Subscriber Growth Rate', 'Hashtags', 'Thumbnail URL']
    df = pd.DataFrame(video_data, columns=columns)
    
    df['HIT_MOV'] = df.apply(lambda row: 'Hit' if (row['View Count'] >= 2*row['Subscriber Count']) and (row['Subscriber Growth Rate'] > 0) else '', axis=1)
    
    # Save as HTML
    table = '<table border="1">\n'
    table += '<tr>\n'
    for col in df.columns:
        table += f'<th>{col}</th>\n'
    table += '</tr>\n'
    for row in df.itertuples(index=False):
        table += '<tr>\n'
        for i, value in enumerate(row):
            if i == 9:  # Thumbnail URL column index
                table += f'<td><img src="{value}" alt="thumbnail"></td>\n'
            elif i == 1:  # URL column index
                table += f'<td><a href="{value}">{value}</a></td>\n'
            else:
                table += f'<td>{value}</td>\n'
        table += '</tr>\n'
    table += '</table>'

    # with open(f'{query}.html', 'w', encoding='utf-8-sig') as f:
    #     f.write(table)
    # Save as CSV
    # df.to_csv(f'{query}.csv', index=False, encoding='utf-8-sig')

    return table


def YoutubeSearch(api_key, keyword):
    youtube = build('youtube', 'v3', developerKey=api_key)
    max_results = 50
    video_data = get_top_videos(youtube, keyword, max_results)
    return save_to_file(video_data, keyword)
