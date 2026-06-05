import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from scipy import stats
import config

def detect_anomalies_zscore(data, column, threshold=3):
    """
    Detect anomalies using Z-score method
    """
    if len(data) < 2:
        return np.zeros(len(data), dtype=bool)
    
    z_scores = np.abs(stats.zscore(data[column], nan_policy='omit'))
    return z_scores > threshold

def detect_anomalies_isolation_forest(df, features):
    """
    Detect anomalies using Isolation Forest algorithm
    """
    if len(df) < 10:  # Need minimum samples for Isolation Forest
        return np.zeros(len(df))
    
    # Prepare features
    X = df[features].fillna(0)
    
    # Train Isolation Forest
    clf = IsolationForest(
        contamination=config.ANOMALY_CONTAMINATION,
        random_state=42,
        n_estimators=100
    )
    
    # -1 for anomalies, 1 for normal
    predictions = clf.fit_predict(X)
    
    # Convert to anomaly scores (0-1 scale, higher = more anomalous)
    scores = clf.score_samples(X)
    normalized_scores = (scores - scores.min()) / (scores.max() - scores.min())
    
    return 1 - normalized_scores  # Invert so higher score = more suspicious

def calculate_engagement_authenticity(df):
    """
    Calculate engagement authenticity based on engagement patterns
    """
    authenticity_scores = []
    
    for influencer in df['influencer_name'].unique():
        influencer_data = df[df['influencer_name'] == influencer]
        
        if len(influencer_data) == 0:
            continue
        
        followers = influencer_data['followers_count'].iloc[0]
        avg_likes = influencer_data['likes'].mean()
        avg_comments = influencer_data['comments_count'].mean()
        
        # Calculate like-to-follower ratio
        like_ratio = (avg_likes / followers * 100) if followers > 0 else 0
        
        # Calculate comment-to-like ratio
        comment_ratio = (avg_comments / avg_likes) if avg_likes > 0 else 0
        
        # Authenticity heuristics
        # Healthy ranges: like_ratio 1-10%, comment_ratio 0.5-5%
        like_score = 1.0 if 1 <= like_ratio <= 10 else max(0, 1 - abs(like_ratio - 5) / 10)
        comment_score = 1.0 if 0.5 <= comment_ratio <= 5 else max(0, 1 - abs(comment_ratio - 2.5) / 5)
        
        authenticity = (like_score + comment_score) / 2
        
        authenticity_scores.append({
            'influencer_name': influencer,
            'engagement_authenticity': round(authenticity, 3),
            'like_ratio': round(like_ratio, 2),
            'comment_ratio': round(comment_ratio, 2)
        })
    
    return pd.DataFrame(authenticity_scores)

def calculate_follower_quality(df):
    """
    Assess follower quality based on follower-to-following ratio
    """
    quality_scores = []
    
    for influencer in df['influencer_name'].unique():
        influencer_data = df[df['influencer_name'] == influencer]
        
        followers = influencer_data['followers_count'].iloc[0]
        following = influencer_data['following_count'].iloc[0]
        
        # Calculate ratio
        if following > 0:
            ratio = followers / following
        else:
            ratio = followers
        
        # Quality score based on ratio
        # Good ratios: > 2 (more followers than following)
        if ratio >= 10:
            quality = 1.0
        elif ratio >= 2:
            quality = 0.8
        elif ratio >= 1:
            quality = 0.6
        elif ratio >= 0.5:
            quality = 0.4
        else:
            quality = 0.2
        
        quality_scores.append({
            'influencer_name': influencer,
            'follower_quality': round(quality, 3),
            'follower_ratio': round(ratio, 2)
        })
    
    return pd.DataFrame(quality_scores)

def detect_spike_anomalies(df):
    """
    Detect unusual spikes in engagement
    """
    spike_detection = []
    
    for influencer in df['influencer_name'].unique():
        influencer_data = df[df['influencer_name'] == influencer].sort_values('timestamp')
        
        if len(influencer_data) < 3:
            spike_detection.append({
                'influencer_name': influencer,
                'spike_detected': False,
                'spike_score': 0.0
            })
            continue
        
        # Detect spikes using Z-score
        engagement = influencer_data['total_engagement'].values
        anomalies = detect_anomalies_zscore(influencer_data, 'total_engagement', threshold=2.5)
        
        spike_score = anomalies.sum() / len(anomalies) if len(anomalies) > 0 else 0
        
        spike_detection.append({
            'influencer_name': influencer,
            'spike_detected': spike_score > 0.2,
            'spike_score': round(spike_score, 3)
        })
    
    return pd.DataFrame(spike_detection)

def estimate_fake_followers(df):
    """
    Estimate the number and percentage of fake followers
    """
    fake_follower_estimates = []
    
    for influencer in df['influencer_name'].unique():
        influencer_data = df[df['influencer_name'] == influencer]
        
        followers = influencer_data['followers_count'].iloc[0]
        following = influencer_data['following_count'].iloc[0]
        avg_likes = influencer_data['likes'].mean()
        avg_comments = influencer_data['comments_count'].mean()
        
        # Calculate suspicious indicators
        like_ratio = (avg_likes / followers * 100) if followers > 0 else 0
        follower_following_ratio = followers / following if following > 0 else followers
        
        # Estimate fake followers based on engagement
        # Normal engagement rate: 1-10%
        expected_min_likes = followers * 0.01  # 1% minimum
        
        fake_percentage = 0
        
        # Low engagement suggests fake followers
        if avg_likes < expected_min_likes:
            engagement_deficit = (expected_min_likes - avg_likes) / expected_min_likes
            fake_percentage += engagement_deficit * 50  # Up to 50% from engagement
        
        # Suspicious follower/following ratio
        if follower_following_ratio < 1:
            fake_percentage += 20  # Add 20% if following more than followers
        elif follower_following_ratio < 2:
            fake_percentage += 10  # Add 10% if ratio is low
        
        # Low comment ratio
        comment_to_like = (avg_comments / avg_likes * 100) if avg_likes > 0 else 0
        if comment_to_like < 0.5:  # Less than 0.5% comments
            fake_percentage += 15
        
        # Cap at 100%
        fake_percentage = min(fake_percentage, 100)
        
        fake_count = int((fake_percentage / 100) * followers)
        real_followers = followers - fake_count
        
        fake_follower_estimates.append({
            'influencer_name': influencer,
            'total_followers': int(followers),
            'estimated_fake_followers': fake_count,
            'estimated_real_followers': real_followers,
            'fake_percentage': round(fake_percentage, 2),
            'real_percentage': round(100 - fake_percentage, 2)
        })
    
    return pd.DataFrame(fake_follower_estimates)

def categorize_follower_authenticity(fake_percentage):
    """
    Categorize follower authenticity based on fake percentage
    """
    if fake_percentage < 10:
        return 'Excellent', '🟢'
    elif fake_percentage < 25:
        return 'Good', '🟡'
    elif fake_percentage < 40:
        return 'Moderate', '🟠'
    elif fake_percentage < 60:
        return 'Poor', '🔴'
    else:
        return 'Very Poor', '⚫'

def detect_fake_followers(df):
    """
    Main function to detect fake followers and calculate credibility score
    """
    print("Detecting fake followers...")
    
    if df.empty or 'influencer_name' not in df.columns:
        return {'error': 'Invalid data provided'}
    
    # Calculate various authenticity metrics
    engagement_auth = calculate_engagement_authenticity(df)
    follower_quality = calculate_follower_quality(df)
    spike_detection = detect_spike_anomalies(df)
    fake_follower_data = estimate_fake_followers(df)
    
    # Merge all scores
    credibility = engagement_auth.merge(follower_quality, on='influencer_name', how='left')
    credibility = credibility.merge(spike_detection, on='influencer_name', how='left')
    credibility = credibility.merge(fake_follower_data, on='influencer_name', how='left')
    
    # Calculate overall credibility score (weighted average)
    credibility['credibility_score'] = (
        credibility['engagement_authenticity'] * 0.4 +
        credibility['follower_quality'] * 0.4 +
        (1 - credibility['spike_score']) * 0.2
    )
    
    credibility['credibility_score'] = credibility['credibility_score'].round(3)
    
    # Classify credibility
    credibility['credibility_status'] = credibility['credibility_score'].apply(
        lambda x: 'High' if x >= 0.7 else ('Medium' if x >= 0.5 else 'Low')
    )
    
    # Add authenticity category and icon
    credibility[['authenticity_category', 'authenticity_icon']] = credibility['fake_percentage'].apply(
        lambda x: pd.Series(categorize_follower_authenticity(x))
    )
    
    # Summary statistics
    summary = {
        'avg_credibility': round(credibility['credibility_score'].mean(), 3),
        'high_credibility_count': int((credibility['credibility_status'] == 'High').sum()),
        'suspicious_count': int((credibility['credibility_status'] == 'Low').sum()),
        'avg_fake_percentage': round(credibility['fake_percentage'].mean(), 2),
        'total_fake_followers': int(credibility['estimated_fake_followers'].sum()),
        'total_real_followers': int(credibility['estimated_real_followers'].sum())
    }
    
    result = {
        'credibility_analysis': credibility.to_dict('records'),
        'summary': summary
    }
    
    print("Fake follower detection complete.")
    return result