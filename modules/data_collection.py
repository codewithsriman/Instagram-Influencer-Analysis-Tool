import requests
import pandas as pd
import config
from datetime import datetime

class InstagramDataCollector:
    def __init__(self, access_token=None):
        self.access_token = access_token or config.INSTAGRAM_ACCESS_TOKEN
        self.base_url = "https://graph.instagram.com/"
    
    def get_user_info(self, user_id):
        """Fetch basic user information"""
        endpoint = f"{self.base_url}{user_id}"
        params = {
            'fields': 'id,username,followers_count,follows_count,media_count',
            'access_token': self.access_token
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching user info: {e}")
            return None
    
    def get_user_media(self, user_id, limit=25):
        """Fetch user's recent media posts"""
        endpoint = f"{self.base_url}{user_id}/media"
        params = {
            'fields': 'id,caption,media_type,media_url,timestamp,like_count,comments_count',
            'limit': limit,
            'access_token': self.access_token
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json().get('data', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching media: {e}")
            return []
    
    def get_media_comments(self, media_id):
        """Fetch comments for a specific media post"""
        endpoint = f"{self.base_url}{media_id}/comments"
        params = {
            'fields': 'id,text,timestamp,username',
            'access_token': self.access_token
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json().get('data', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching comments: {e}")
            return []
    
    def collect_influencer_data(self, user_id, influencer_name):
        """Collect complete influencer dataset"""
        print(f"Collecting data for {influencer_name}...")
        
        # Get user info
        user_info = self.get_user_info(user_id)
        if not user_info:
            return None
        
        # Get media posts
        media_posts = self.get_user_media(user_id)
        
        # Compile data
        data_records = []
        for post in media_posts:
            comments = self.get_media_comments(post['id'])
            
            record = {
                'influencer_name': influencer_name,
                'user_id': user_id,
                'followers_count': user_info.get('followers_count', 0),
                'following_count': user_info.get('follows_count', 0),
                'total_posts': user_info.get('media_count', 0),
                'post_id': post['id'],
                'post_type': post.get('media_type', 'IMAGE'),
                'likes': post.get('like_count', 0),
                'comments_count': post.get('comments_count', 0),
                'timestamp': post.get('timestamp', ''),
                'caption': post.get('caption', ''),
                'comments': [c['text'] for c in comments]
            }
            data_records.append(record)
        
        return pd.DataFrame(data_records)
    
    def save_to_csv(self, df, filename='data/collected_data.csv'):
        """Save collected data to CSV"""
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

def collect_data(user_ids=None, influencer_names=None):
    """Main function to collect data for multiple influencers"""
    collector = InstagramDataCollector()
    
    if not user_ids or not config.INSTAGRAM_ACCESS_TOKEN:
        print("No API credentials or user IDs provided. Using sample data.")
        return pd.read_csv(config.SAMPLE_DATA_PATH)
    
    all_data = []
    for user_id, name in zip(user_ids, influencer_names):
        df = collector.collect_influencer_data(user_id, name)
        if df is not None:
            all_data.append(df)
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        collector.save_to_csv(combined_df)
        return combined_df
    
    return None