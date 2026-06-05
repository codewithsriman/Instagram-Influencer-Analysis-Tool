import pandas as pd
import numpy as np

def compute_engagement_rate(df):
    """
    Calculate engagement rate for each influencer
    Engagement Rate = (Total Engagement / Followers) * 100
    """
    engagement_rates = []
    
    for influencer in df['influencer_name'].unique():
        influencer_data = df[df['influencer_name'] == influencer]
        
        total_engagement = influencer_data['total_engagement'].sum()
        followers = influencer_data['followers_count'].iloc[0]
        num_posts = len(influencer_data)
        
        if followers > 0 and num_posts > 0:
            engagement_rate = (total_engagement / (followers * num_posts)) * 100
        else:
            engagement_rate = 0
        
        engagement_rates.append({
            'influencer_name': influencer,
            'engagement_rate': round(engagement_rate, 2),
            'avg_engagement_per_post': round(total_engagement / num_posts, 2) if num_posts > 0 else 0
        })
    
    return pd.DataFrame(engagement_rates)

def compute_follower_growth(df):
    """
    Calculate follower growth rate over time
    Note: Requires historical data. This is a simplified version.
    """
    growth_data = []
    
    for influencer in df['influencer_name'].unique():
        influencer_data = df[df['influencer_name'] == influencer].sort_values('timestamp')
        
        if len(influencer_data) > 1:
            # Simulate growth based on engagement trends (in real scenario, use historical follower counts)
            first_engagement = influencer_data['total_engagement'].iloc[0]
            last_engagement = influencer_data['total_engagement'].iloc[-1]
            
            if first_engagement > 0:
                growth_indicator = ((last_engagement - first_engagement) / first_engagement) * 100
            else:
                growth_indicator = 0
        else:
            growth_indicator = 0
        
        growth_data.append({
            'influencer_name': influencer,
            'growth_indicator': round(growth_indicator, 2)
        })
    
    return pd.DataFrame(growth_data)

def compute_reach_metrics(df):
    """
    Calculate reach and impression metrics
    """
    reach_metrics = []
    
    for influencer in df['influencer_name'].unique():
        influencer_data = df[df['influencer_name'] == influencer]
        
        total_likes = influencer_data['likes'].sum()
        total_comments = influencer_data['comments_count'].sum()
        followers = influencer_data['followers_count'].iloc[0]
        num_posts = len(influencer_data)
        
        avg_reach = (total_likes + total_comments) / num_posts if num_posts > 0 else 0
        reach_percentage = (avg_reach / followers * 100) if followers > 0 else 0
        
        reach_metrics.append({
            'influencer_name': influencer,
            'avg_reach': round(avg_reach, 2),
            'reach_percentage': round(reach_percentage, 2),
            'total_likes': int(total_likes),
            'total_comments': int(total_comments)
        })
    
    return pd.DataFrame(reach_metrics)

def compute_consistency_score(df):
    """
    Calculate posting consistency and engagement consistency
    """
    consistency_scores = []
    
    for influencer in df['influencer_name'].unique():
        influencer_data = df[df['influencer_name'] == influencer].sort_values('timestamp')
        
        # Calculate coefficient of variation for engagement
        engagement_std = influencer_data['total_engagement'].std()
        engagement_mean = influencer_data['total_engagement'].mean()
        
        if engagement_mean > 0:
            consistency = (1 - (engagement_std / engagement_mean)) * 100
            consistency = max(0, min(100, consistency))  # Bound between 0-100
        else:
            consistency = 0
        
        consistency_scores.append({
            'influencer_name': influencer,
            'consistency_score': round(consistency, 2)
        })
    
    return pd.DataFrame(consistency_scores)

def compute_metrics(df):
    """
    Main function to compute all metrics
    Returns a comprehensive metrics dictionary
    """
    print("Computing metrics...")
    
    if df.empty or 'influencer_name' not in df.columns:
        return {'error': 'Invalid data provided'}
    
    # Calculate all metrics
    engagement = compute_engagement_rate(df)
    growth = compute_follower_growth(df)
    reach = compute_reach_metrics(df)
    consistency = compute_consistency_score(df)
    
    # Merge all metrics
    metrics = engagement.merge(growth, on='influencer_name', how='left')
    metrics = metrics.merge(reach, on='influencer_name', how='left')
    metrics = metrics.merge(consistency, on='influencer_name', how='left')
    
    # Add summary statistics
    summary = {
        'total_influencers': len(metrics),
        'avg_engagement_rate': round(metrics['engagement_rate'].mean(), 2),
        'avg_reach_percentage': round(metrics['reach_percentage'].mean(), 2),
        'avg_consistency': round(metrics['consistency_score'].mean(), 2)
    }
    
    result = {
        'influencer_metrics': metrics.to_dict('records'),
        'summary': summary
    }
    
    print("Metrics computation complete.")
    return result