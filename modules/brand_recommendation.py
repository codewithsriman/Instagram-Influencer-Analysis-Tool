import pandas as pd
import numpy as np

# Brand Database by Niche
BRAND_DATABASE = {
    'fashion': {
        'brands': ['Zara', 'H&M', 'Myntra', 'Forever 21', 'Mango', 'Urbanic', 'Shein', 'Ajio'],
        'multiplier': 1.2
    },
    'beauty': {
        'brands': ["Nykaa", "L'Oréal", 'Maybelline', 'MAC', 'Lakme', 'Sugar Cosmetics', 'Huda Beauty', 'Faces Canada'],
        'multiplier': 1.5
    },
    'fitness': {
        'brands': ['Nike', 'Adidas', 'Puma', 'Reebok', 'Under Armour', 'Decathlon', 'Cult.fit', 'HealthifyMe'],
        'multiplier': 1.1
    },
    'travel': {
        'brands': ['MakeMyTrip', 'Airbnb', 'Booking.com', 'TripAdvisor', 'OYO', 'Cleartrip', 'Goibibo', 'Yatra'],
        'multiplier': 1.3
    },
    'tech': {
        'brands': ['Apple', 'Samsung', 'OnePlus', 'Xiaomi', 'Realme', 'Amazon', 'Flipkart', 'Google'],
        'multiplier': 1.4
    },
    'food': {
        'brands': ['Swiggy', 'Zomato', 'Dominos', 'McDonalds', 'KFC', 'Starbucks', 'Dunkin', 'Blinkit'],
        'multiplier': 1.0
    },
    'lifestyle': {
        'brands': ['Amazon', 'Flipkart', 'Urban Ladder', 'Pepperfry', 'IKEA', 'Fabindia', 'Westside', 'Shoppers Stop'],
        'multiplier': 1.1
    },
    'gaming': {
        'brands': ['PlayStation', 'Xbox', 'Nintendo', 'Razer', 'Logitech', 'Twitch', 'Discord', 'Steam'],
        'multiplier': 1.3
    }
}

# Collaboration Types
COLLABORATION_TYPES = [
    {
        'type': 'Sponsored Post',
        'description': 'Single post featuring brand/product',
        'min_followers': 5000,
        'engagement_threshold': 2.0
    },
    {
        'type': 'Product Review',
        'description': 'Detailed review with unboxing/demo',
        'min_followers': 10000,
        'engagement_threshold': 2.5
    },
    {
        'type': 'Reel Promotion',
        'description': 'Short-form video content promotion',
        'min_followers': 15000,
        'engagement_threshold': 3.0
    },
    {
        'type': 'Story Collaboration',
        'description': 'Instagram Stories feature (24hr)',
        'min_followers': 5000,
        'engagement_threshold': 2.0
    },
    {
        'type': 'Ambassador Program',
        'description': 'Long-term brand partnership',
        'min_followers': 50000,
        'engagement_threshold': 4.0
    },
    {
        'type': 'Giveaway Partnership',
        'description': 'Contest/giveaway collaboration',
        'min_followers': 10000,
        'engagement_threshold': 3.5
    }
]

def detect_influencer_niche(df, influencer_name):
    """
    Detect influencer niche based on captions and hashtags
    """
    influencer_data = df[df['influencer_name'] == influencer_name]
    
    if influencer_data.empty:
        return 'lifestyle'
    
    # Analyze captions for keywords
    captions = ' '.join(influencer_data['caption'].fillna('').astype(str).tolist()).lower()
    
    niche_keywords = {
        'fashion': ['fashion', 'style', 'outfit', 'dress', 'clothing', 'wear', 'trend', 'ootd'],
        'beauty': ['makeup', 'beauty', 'skincare', 'cosmetic', 'lipstick', 'foundation', 'skincare'],
        'fitness': ['fitness', 'workout', 'gym', 'health', 'exercise', 'training', 'muscle', 'yoga'],
        'travel': ['travel', 'trip', 'destination', 'explore', 'adventure', 'vacation', 'journey'],
        'tech': ['tech', 'technology', 'gadget', 'phone', 'laptop', 'software', 'app', 'device'],
        'food': ['food', 'recipe', 'cooking', 'eat', 'delicious', 'restaurant', 'meal', 'cuisine'],
        'gaming': ['gaming', 'game', 'gamer', 'play', 'stream', 'esports', 'console'],
        'lifestyle': ['life', 'daily', 'vlog', 'day', 'routine', 'living']
    }
    
    niche_scores = {}
    for niche, keywords in niche_keywords.items():
        score = sum(captions.count(keyword) for keyword in keywords)
        niche_scores[niche] = score
    
    detected_niche = max(niche_scores, key=niche_scores.get)
    return detected_niche if niche_scores[detected_niche] > 0 else 'lifestyle'

def analyze_audience_demographics(df, influencer_name):
    """
    Simulate audience demographics analysis
    In production, this would use Instagram Insights API
    """
    influencer_data = df[df['influencer_name'] == influencer_name]
    
    if influencer_data.empty:
        return {
            'age_groups': {'18-24': 30, '25-34': 40, '35-44': 20, '45+': 10},
            'gender': {'Female': 60, 'Male': 40},
            'top_countries': ['India', 'USA', 'UK'],
            'interests': ['Fashion', 'Lifestyle', 'Entertainment']
        }
    
    # Simulate based on engagement patterns
    avg_engagement = influencer_data['total_engagement'].mean()
    
    # Higher engagement suggests younger audience
    if avg_engagement > 500:
        age_groups = {'18-24': 45, '25-34': 35, '35-44': 15, '45+': 5}
    else:
        age_groups = {'18-24': 25, '25-34': 40, '35-44': 25, '45+': 10}
    
    return {
        'age_groups': age_groups,
        'gender': {'Female': 55, 'Male': 45},
        'top_countries': ['India', 'USA', 'UAE'],
        'interests': ['Fashion', 'Lifestyle', 'Travel', 'Food']
    }

def calculate_collaboration_price(followers, engagement_rate, niche, credibility_score):
    """
    Calculate estimated collaboration price range
    Formula considers: followers, engagement, niche value, credibility
    """
    # Base price calculation (INR)
    if followers < 10000:
        base_price = followers * 2
    elif followers < 50000:
        base_price = followers * 1.5
    elif followers < 100000:
        base_price = followers * 1.2
    else:
        base_price = followers * 1.0
    
    # Engagement rate multiplier (2-10% is good)
    if engagement_rate > 5:
        engagement_multiplier = 1.5
    elif engagement_rate > 3:
        engagement_multiplier = 1.3
    elif engagement_rate > 2:
        engagement_multiplier = 1.1
    else:
        engagement_multiplier = 0.9
    
    # Niche multiplier
    niche_multiplier = BRAND_DATABASE.get(niche, {'multiplier': 1.0})['multiplier']
    
    # Credibility multiplier
    credibility_multiplier = 0.8 + (credibility_score * 0.4)
    
    # Calculate final price
    estimated_price = base_price * engagement_multiplier * niche_multiplier * credibility_multiplier
    
    # Price range (±20%)
    min_price = int(estimated_price * 0.8)
    max_price = int(estimated_price * 1.2)
    
    return {
        'min_price': min_price,
        'max_price': max_price,
        'currency': 'INR'
    }

def recommend_collaboration_types(followers, engagement_rate, credibility_score):
    """
    Recommend suitable collaboration types based on metrics
    """
    suitable_types = []
    
    for collab in COLLABORATION_TYPES:
        if followers >= collab['min_followers'] and engagement_rate >= collab['engagement_threshold']:
            score = (engagement_rate / 10) * 0.5 + credibility_score * 0.5
            
            suitable_types.append({
                'type': collab['type'],
                'description': collab['description'],
                'suitability_score': round(min(score, 1.0), 2)
            })
    
    # Sort by suitability score
    suitable_types.sort(key=lambda x: x['suitability_score'], reverse=True)
    
    return suitable_types[:3]  # Return top 3

def generate_brand_recommendations(df, influencer_name, metrics, credibility, sentiment):
    """
    Main function to generate AI-powered brand collaboration recommendations
    """
    print(f"Generating brand recommendations for {influencer_name}...")
    
    # Get influencer data
    influencer_data = df[df['influencer_name'] == influencer_name]
    
    if influencer_data.empty:
        return {'error': 'Influencer not found'}
    
    # Extract metrics
    followers = influencer_data['followers_count'].iloc[0]
    
    # Find engagement rate from metrics
    influencer_metrics = next(
        (m for m in metrics['influencer_metrics'] if m['influencer_name'] == influencer_name),
        {}
    )
    engagement_rate = influencer_metrics.get('engagement_rate', 0)
    
    # Find credibility score
    influencer_credibility = next(
        (c for c in credibility['credibility_analysis'] if c['influencer_name'] == influencer_name),
        {}
    )
    credibility_score = influencer_credibility.get('credibility_score', 0.5)
    
    # Detect niche
    niche = detect_influencer_niche(df, influencer_name)
    
    # Analyze audience
    audience_demographics = analyze_audience_demographics(df, influencer_name)
    
    # Get matching brands
    matching_brands = BRAND_DATABASE.get(niche, {'brands': ['General Brands']})['brands']
    
    # Recommend collaboration types
    collaboration_types = recommend_collaboration_types(followers, engagement_rate, credibility_score)
    
    # Calculate price range
    price_range = calculate_collaboration_price(followers, engagement_rate, niche, credibility_score)
    
    # Compile recommendations
    recommendations = {
        'influencer_name': influencer_name,
        'niche': niche.title(),
        'audience_demographics': audience_demographics,
        'recommended_brands': matching_brands[:8],
        'collaboration_types': collaboration_types,
        'estimated_price_range': price_range,
        'metrics_summary': {
            'followers': int(followers),
            'engagement_rate': engagement_rate,
            'credibility_score': credibility_score,
            'credibility_status': influencer_credibility.get('credibility_status', 'Medium')
        }
    }
    
    print("Brand recommendations generated successfully.")
    return recommendations