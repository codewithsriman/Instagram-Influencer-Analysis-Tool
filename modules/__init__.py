# modules/__init__.py
"""
Instagram Influencer Impact Analysis Modules
"""

from modules.data_collection import collect_data
from modules.data_preprocessing import preprocess_data
from modules.metrics_computation import compute_metrics
from modules.fake_follower_detection import detect_fake_followers
from modules.sentiment_analysis import analyze_sentiment
from modules.user_search import get_influencer_profile, get_all_influencers_list
from modules.brand_recommendation import generate_brand_recommendations
from modules.auth import (
    save_user, verify_user, get_user, update_user_profile,
    generate_token, verify_token, token_required, init_users_file
)

__all__ = [
    'collect_data',
    'preprocess_data',
    'compute_metrics',
    'detect_fake_followers',
    'analyze_sentiment',
    'get_influencer_profile',
    'get_all_influencers_list',
    'generate_brand_recommendations',
    'save_user',
    'verify_user',
    'get_user',
    'update_user_profile',
    'generate_token',
    'verify_token',
    'token_required',
    'init_users_file'
]

# -------------------

# utils/__init__.py
"""
Utility Functions
"""

from utils.helpers import (
    load_sample_data,
    generate_sample_data,
    save_to_json,
    load_from_json,
    format_number,
    calculate_growth_rate,
    validate_email,
    sanitize_input,
    get_date_range,
    export_to_csv,
    create_backup
)

__all__ = [
    'load_sample_data',
    'generate_sample_data',
    'save_to_json',
    'load_from_json',
    'format_number',
    'calculate_growth_rate',
    'validate_email',
    'sanitize_input',
    'get_date_range',
    'export_to_csv',
    'create_backup'
]