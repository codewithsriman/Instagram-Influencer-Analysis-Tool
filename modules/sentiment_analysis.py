import pandas as pd
import numpy as np
from textblob import TextBlob
import re

def clean_text(text):
    """
    Clean text for sentiment analysis
    """
    if not isinstance(text, str):
        return ""
    
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove mentions and hashtags
    text = re.sub(r'@\w+|#\w+', '', text)
    
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Convert to lowercase and strip whitespace
    text = text.lower().strip()
    
    return text

def analyze_text_sentiment(text):
    """
    Analyze sentiment of a single text using TextBlob
    Returns polarity (-1 to 1) and subjectivity (0 to 1)
    """
    if not text or len(text.strip()) == 0:
        return {'polarity': 0, 'subjectivity': 0, 'sentiment': 'neutral'}
    
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Classify sentiment
    if polarity > 0.1:
        sentiment = 'positive'
    elif polarity < -0.1:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    
    return {
        'polarity': round(polarity, 3),
        'subjectivity': round(subjectivity, 3),
        'sentiment': sentiment
    }

def analyze_comments_sentiment(comments_list):
    """
    Analyze sentiment for a list of comments
    """
    if not comments_list or len(comments_list) == 0:
        return {
            'avg_polarity': 0,
            'avg_subjectivity': 0,
            'positive_count': 0,
            'negative_count': 0,
            'neutral_count': 0,
            'dominant_sentiment': 'neutral'
        }
    
    sentiments = []
    for comment in comments_list:
        cleaned = clean_text(str(comment))
        if cleaned:
            sentiment = analyze_text_sentiment(cleaned)
            sentiments.append(sentiment)
    
    if not sentiments:
        return {
            'avg_polarity': 0,
            'avg_subjectivity': 0,
            'positive_count': 0,
            'negative_count': 0,
            'neutral_count': 0,
            'dominant_sentiment': 'neutral'
        }
    
    # Calculate statistics
    polarities = [s['polarity'] for s in sentiments]
    subjectivities = [s['subjectivity'] for s in sentiments]
    sentiment_labels = [s['sentiment'] for s in sentiments]
    
    positive_count = sentiment_labels.count('positive')
    negative_count = sentiment_labels.count('negative')
    neutral_count = sentiment_labels.count('neutral')
    
    # Determine dominant sentiment
    max_count = max(positive_count, negative_count, neutral_count)
    if positive_count == max_count:
        dominant = 'positive'
    elif negative_count == max_count:
        dominant = 'negative'
    else:
        dominant = 'neutral'
    
    return {
        'avg_polarity': round(np.mean(polarities), 3),
        'avg_subjectivity': round(np.mean(subjectivities), 3),
        'positive_count': positive_count,
        'negative_count': negative_count,
        'neutral_count': neutral_count,
        'dominant_sentiment': dominant,
        'total_comments': len(sentiments)
    }

def analyze_caption_sentiment(df):
    """
    Analyze sentiment of post captions
    """
    caption_sentiments = []
    
    for influencer in df['influencer_name'].unique():
        influencer_data = df[df['influencer_name'] == influencer]
        
        captions = influencer_data['caption'].tolist()
        polarities = []
        
        for caption in captions:
            cleaned = clean_text(str(caption))
            if cleaned:
                sentiment = analyze_text_sentiment(cleaned)
                polarities.append(sentiment['polarity'])
        
        avg_polarity = np.mean(polarities) if polarities else 0
        
        caption_sentiments.append({
            'influencer_name': influencer,
            'caption_sentiment': round(avg_polarity, 3),
            'caption_tone': 'positive' if avg_polarity > 0.1 else ('negative' if avg_polarity < -0.1 else 'neutral')
        })
    
    return pd.DataFrame(caption_sentiments)

def analyze_sentiment(df):
    """
    Main function to analyze sentiment across all influencers
    """
    print("Analyzing sentiment...")
    
    if df.empty or 'influencer_name' not in df.columns:
        return {'error': 'Invalid data provided'}
    
    sentiment_results = []
    
    for influencer in df['influencer_name'].unique():
        influencer_data = df[df['influencer_name'] == influencer]
        
        # Analyze comments sentiment
        all_comments = []
        if 'comments' in influencer_data.columns:
            for comments in influencer_data['comments']:
                if isinstance(comments, list):
                    all_comments.extend(comments)
                elif isinstance(comments, str) and len(comments) > 0:
                    all_comments.append(comments)
        
        comment_sentiment = analyze_comments_sentiment(all_comments)
        
        # Analyze caption sentiment
        captions = influencer_data['caption'].tolist()
        caption_polarities = []
        
        for caption in captions:
            cleaned = clean_text(str(caption))
            if cleaned:
                sentiment = analyze_text_sentiment(cleaned)
                caption_polarities.append(sentiment['polarity'])
        
        avg_caption_polarity = np.mean(caption_polarities) if caption_polarities else 0
        
        # Compile results
        sentiment_results.append({
            'influencer_name': influencer,
            'comment_sentiment': comment_sentiment['dominant_sentiment'],
            'avg_comment_polarity': comment_sentiment['avg_polarity'],
            'positive_comments_pct': round((comment_sentiment['positive_count'] / comment_sentiment['total_comments'] * 100) if comment_sentiment['total_comments'] > 0 else 0, 2),
            'negative_comments_pct': round((comment_sentiment['negative_count'] / comment_sentiment['total_comments'] * 100) if comment_sentiment['total_comments'] > 0 else 0, 2),
            'caption_sentiment': 'positive' if avg_caption_polarity > 0.1 else ('negative' if avg_caption_polarity < -0.1 else 'neutral'),
            'avg_caption_polarity': round(avg_caption_polarity, 3),
            'total_comments_analyzed': comment_sentiment['total_comments']
        })
    
    # Calculate summary
    sentiment_df = pd.DataFrame(sentiment_results)
    
    summary = {
        'avg_comment_polarity': round(sentiment_df['avg_comment_polarity'].mean(), 3),
        'avg_caption_polarity': round(sentiment_df['avg_caption_polarity'].mean(), 3),
        'positive_influencers': int((sentiment_df['comment_sentiment'] == 'positive').sum()),
        'negative_influencers': int((sentiment_df['comment_sentiment'] == 'negative').sum())
    }
    
    result = {
        'sentiment_analysis': sentiment_results,
        'summary': summary
    }
    
    print("Sentiment analysis complete.")
    return result