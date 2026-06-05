import pandas as pd
import numpy as np
from modules.data_preprocessing import preprocess_data
from modules.metrics_computation import compute_metrics
from modules.fake_follower_detection import detect_fake_followers
from modules.sentiment_analysis import analyze_sentiment

def search_influencer_by_username(df, username):
    """
    Search for influencer by username and return detailed profile
    """
    print(f"Searching for influencer: {username}")
    
    # Search for the influencer (case-insensitive)
    influencer_data = df[df['influencer_name'].str.lower() == username.lower()]
    
    if influencer_data.empty:
        return None
    
    return influencer_data

def get_influencer_profile(df, username):
    """
    Get comprehensive influencer profile with all analytics
    """
    influencer_data = search_influencer_by_username(df, username)
    
    if influencer_data is None:
        return {'status': 'error', 'message': 'Influencer not found'}
    
    # Preprocess data
    cleaned_data = preprocess_data(influencer_data)
    
    # Compute metrics
    metrics = compute_metrics(cleaned_data)
    
    # Detect fake followers
    credibility = detect_fake_followers(cleaned_data)
    
    # Analyze sentiment
    sentiment = analyze_sentiment(cleaned_data)
    
    # Get basic profile info
    profile_info = {
        'username': username,
        'profile_photo': 'default-influencer.png',  # In production, fetch from API
        'followers_count': int(influencer_data['followers_count'].iloc[0]),
        'following_count': int(influencer_data['following_count'].iloc[0]),
        'total_posts': int(influencer_data['total_posts'].iloc[0])
    }
    
    # Get recent posts
    recent_posts = []
    for idx, post in influencer_data.head(6).iterrows():
        recent_posts.append({
            'post_id': str(post.get('post_id', idx)),
            'likes': int(post.get('likes', 0)),
            'comments': int(post.get('comments_count', 0)),
            'caption': str(post.get('caption', ''))[:100] + '...' if len(str(post.get('caption', ''))) > 100 else str(post.get('caption', '')),
            'timestamp': str(post.get('timestamp', ''))
        })
    
    # Calculate engagement trend
    if len(influencer_data) > 1:
        influencer_data_sorted = influencer_data.sort_values('timestamp')
        engagement_trend = influencer_data_sorted['total_engagement'].tolist()[-10:]  # Last 10 posts
    else:
        engagement_trend = []
    
    # Compile complete profile
    profile = {
        'status': 'success',
        'profile_info': profile_info,
        'metrics': metrics,
        'credibility': credibility,
        'sentiment': sentiment,
        'recent_posts': recent_posts,
        'engagement_trend': engagement_trend
    }
    
    return profile

def get_all_influencers_list(df):
    """
    Get list of all available influencers for search suggestions
    """
    if df.empty or 'influencer_name' not in df.columns:
        return []
    
    influencers = df['influencer_name'].unique().tolist()
    
    # Get basic stats for each
    influencer_list = []
    for name in influencers:
        influencer_df = df[df['influencer_name'] == name]
        influencer_list.append({
            'username': name,
            'followers': int(influencer_df['followers_count'].iloc[0]),
            'total_posts': int(influencer_df['total_posts'].iloc[0])
        })
    
    return influencer_list