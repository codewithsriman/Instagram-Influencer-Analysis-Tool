import pandas as pd
import os
import json
from datetime import datetime, timedelta
import random

def load_sample_data():
    """
    Load sample data from CSV or generate if not exists
    """
    sample_path = 'data/sample_data.csv'
    
    if os.path.exists(sample_path):
        try:
            df = pd.read_csv(sample_path)
            
            # Convert comments from string to list if needed
            if 'comments' in df.columns:
                df['comments'] = df['comments'].apply(lambda x: eval(x) if isinstance(x, str) and x.startswith('[') else [])
            
            return df
        except Exception as e:
            print(f"Error loading sample data: {e}")
            return generate_sample_data()
    else:
        print("Sample data not found. Generating sample data...")
        return generate_sample_data()

def generate_sample_data():
    """
    Generate sample influencer data for demonstration
    """
    influencers = [
        'fashionista_maya',
        'tech_guru_raj',
        'fitness_freak_anjali',
        'travel_tales_rohit',
        'foodie_priya'
    ]
    
    data_records = []
    base_date = datetime.now()
    
    for influencer in influencers:
        # Random follower counts
        followers = random.randint(50000, 500000)
        following = random.randint(500, 5000)
        total_posts = random.randint(100, 500)
        
        # Generate 15-20 posts per influencer
        num_posts = random.randint(15, 20)
        
        for i in range(num_posts):
            post_date = base_date - timedelta(days=random.randint(1, 90))
            
            # Generate realistic engagement
            likes = int(followers * random.uniform(0.02, 0.08))
            comments = int(likes * random.uniform(0.005, 0.02))
            
            # Generate sample comments
            sample_comments = generate_sample_comments(random.randint(3, 8))
            
            record = {
                'influencer_name': influencer,
                'user_id': f'user_{influencer}',
                'followers_count': followers,
                'following_count': following,
                'total_posts': total_posts,
                'post_id': f'post_{influencer}_{i}',
                'post_type': random.choice(['IMAGE', 'VIDEO', 'CAROUSEL']),
                'likes': likes,
                'comments_count': comments,
                'timestamp': post_date.isoformat(),
                'caption': generate_sample_caption(influencer),
                'comments': sample_comments,
                'total_engagement': likes + comments
            }
            
            data_records.append(record)
    
    df = pd.DataFrame(data_records)
    
    # Save to CSV
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/sample_data.csv', index=False)
    print(f"Sample data generated with {len(df)} records")
    
    return df

def generate_sample_caption(influencer_name):
    """Generate sample captions based on influencer type"""
    captions = {
        'fashionista': [
            'New collection alert! Check out this stunning outfit',
            'Fashion trends for this season',
            'Style inspiration for the weekend',
            'Loving this new look! What do you think?'
        ],
        'tech': [
            'Latest gadget review! This is game-changing',
            'Tech tips and tricks you need to know',
            'Unboxing the newest smartphone',
            'My thoughts on this revolutionary device'
        ],
        'fitness': [
            'Morning workout routine to start your day',
            'Fitness motivation for the week',
            'Healthy lifestyle tips',
            'New personal record at the gym today!'
        ],
        'travel': [
            'Exploring hidden gems in this beautiful city',
            'Travel guide to amazing destinations',
            'Weekend getaway inspiration',
            'Adventures and wanderlust'
        ],
        'foodie': [
            'Delicious recipe you must try',
            'Food review at this amazing restaurant',
            'Cooking tips and tricks',
            'Foodie adventures continue!'
        ]
    }
    
    # Detect influencer type
    for key in captions.keys():
        if key in influencer_name.lower():
            return random.choice(captions[key])
    
    return 'Check out my latest post!'

def generate_sample_comments(count=5):
    """Generate sample comments with various sentiments"""
    positive_comments = [
        'Absolutely love this!',
        'Amazing content!',
        'You are so inspiring!',
        'This is incredible!',
        'Great work!',
        'Beautiful!',
        'So good!',
        'Love it!'
    ]
    
    neutral_comments = [
        'Nice post',
        'Interesting',
        'Thanks for sharing',
        'Good content',
        'Cool'
    ]
    
    negative_comments = [
        'Not my favorite',
        'Could be better',
        'Meh',
        'Not impressed'
    ]
    
    all_comments = positive_comments * 7 + neutral_comments * 2 + negative_comments * 1
    
    return random.sample(all_comments, min(count, len(all_comments)))

def save_to_json(data, filename):
    """Save data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def load_from_json(filename):
    """Load data from JSON file"""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def format_number(num):
    """Format large numbers for display"""
    if num >= 1000000:
        return f"{num/1000000:.1f}M"
    elif num >= 1000:
        return f"{num/1000:.1f}K"
    return str(num)

def calculate_growth_rate(current, previous):
    """Calculate growth rate percentage"""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

def validate_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_input(text):
    """Sanitize user input"""
    if not isinstance(text, str):
        return ""
    
    # Remove potentially harmful characters
    text = text.strip()
    text = text.replace('<', '').replace('>', '')
    text = text.replace('script', '').replace('javascript:', '')
    
    return text

def get_date_range(days=30):
    """Get date range for filtering"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date

def export_to_csv(data, filename):
    """Export data to CSV"""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    return filename

def create_backup(source_file, backup_dir='backups'):
    """Create backup of important files"""
    if not os.path.exists(source_file):
        return None
    
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.basename(source_file)
    backup_path = os.path.join(backup_dir, f"{filename}.{timestamp}.bak")
    
    import shutil
    shutil.copy2(source_file, backup_path)
    
    return backup_path