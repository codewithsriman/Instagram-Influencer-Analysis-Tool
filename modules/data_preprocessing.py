import pandas as pd
import numpy as np
from datetime import datetime

def preprocess_data(df):
    """
    Clean and normalize influencer data
    - Remove duplicates
    - Handle missing values
    - Normalize data types
    - Create derived features
    """
    print("Starting data preprocessing...")
    
    # Create a copy to avoid modifying original
    data = df.copy()
    
    # Remove duplicate posts
    if 'post_id' in data.columns:
        data = data.drop_duplicates(subset=['post_id'], keep='first')
        print(f"Removed {len(df) - len(data)} duplicate posts")
    
    # Handle missing values
    numeric_columns = ['followers_count', 'following_count', 'likes', 'comments_count', 'total_posts']
    for col in numeric_columns:
        if col in data.columns:
            data[col] = data[col].fillna(0)
            data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
    
    # Fill missing text data
    text_columns = ['caption', 'influencer_name']
    for col in text_columns:
        if col in data.columns:
            data[col] = data[col].fillna('')
    
    # Convert timestamp to datetime
    if 'timestamp' in data.columns:
        data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')
        data['date'] = data['timestamp'].dt.date
        data['hour'] = data['timestamp'].dt.hour
        data['day_of_week'] = data['timestamp'].dt.dayofweek
    
    # Calculate engagement per post
    if 'likes' in data.columns and 'comments_count' in data.columns:
        data['total_engagement'] = data['likes'] + data['comments_count']
    
    # Calculate follower-to-following ratio
    if 'followers_count' in data.columns and 'following_count' in data.columns:
        data['follower_ratio'] = np.where(
            data['following_count'] > 0,
            data['followers_count'] / data['following_count'],
            data['followers_count']
        )
    
    # Remove rows with critical missing data
    if 'influencer_name' in data.columns:
        data = data[data['influencer_name'].str.len() > 0]
    
    # Sort by timestamp
    if 'timestamp' in data.columns:
        data = data.sort_values('timestamp', ascending=False)
    
    # Reset index
    data = data.reset_index(drop=True)
    
    print(f"Preprocessing complete. Final dataset: {len(data)} rows, {len(data.columns)} columns")
    
    return data

def create_aggregated_metrics(df):
    """
    Create aggregated metrics per influencer
    """
    if df.empty:
        return pd.DataFrame()
    
    agg_dict = {
        'followers_count': 'first',
        'following_count': 'first',
        'total_posts': 'first',
        'likes': ['mean', 'sum', 'std'],
        'comments_count': ['mean', 'sum', 'std'],
        'total_engagement': ['mean', 'sum']
    }
    
    # Filter aggregation dict to only include existing columns
    agg_dict = {k: v for k, v in agg_dict.items() if k in df.columns}
    
    aggregated = df.groupby('influencer_name').agg(agg_dict).reset_index()
    
    # Flatten column names
    aggregated.columns = ['_'.join(col).strip('_') for col in aggregated.columns.values]
    
    return aggregated

def normalize_features(df, columns):
    """
    Normalize numerical features using min-max scaling
    """
    data = df.copy()
    
    for col in columns:
        if col in data.columns:
            min_val = data[col].min()
            max_val = data[col].max()
            
            if max_val > min_val:
                data[f'{col}_normalized'] = (data[col] - min_val) / (max_val - min_val)
            else:
                data[f'{col}_normalized'] = 0
    
    return data