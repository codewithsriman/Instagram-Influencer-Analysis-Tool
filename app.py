from flask import Flask, render_template, jsonify, request
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from modules.data_collection import collect_data
    from modules.data_preprocessing import preprocess_data
    from modules.metrics_computation import compute_metrics
    from modules.fake_follower_detection import detect_fake_followers
    from modules.sentiment_analysis import analyze_sentiment
    from utils.helpers import load_sample_data
    import config
    import pandas as pd
except ImportError as e:
    print(f"Import Error: {e}")
    print("Please ensure all modules are in the correct directories")
    sys.exit(1)

app = Flask(__name__)

try:
    app.config.from_object(config)
except Exception as e:
    print(f"Configuration Error: {e}")
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['DEBUG'] = True

# ============= Page Routes =============

@app.route('/')
def index():
    """Login page"""
    return render_template('login.html')

@app.route('/signup')
def signup_page():
    """Signup page"""
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/profile')
def profile_page():
    """User profile page"""
    return render_template('profile.html')

# ============= API Routes =============

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze all influencers"""
    try:
        # Load data
        data = load_sample_data()
        
        # Preprocess data
        cleaned_data = preprocess_data(data)
        
        # Compute metrics
        metrics = compute_metrics(cleaned_data)
        
        # Detect fake followers
        credibility = detect_fake_followers(cleaned_data)
        
        # Analyze sentiment
        sentiment = analyze_sentiment(cleaned_data)
        
        response = {
            'metrics': metrics,
            'credibility': credibility,
            'sentiment': sentiment,
            'status': 'success'
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error in /api/analyze: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/influencers', methods=['GET'])
def get_influencers():
    """Get list of all influencers"""
    try:
        data = load_sample_data()
        influencers = data['influencer_name'].unique().tolist()
        return jsonify({'influencers': influencers})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/influencer/<name>', methods=['GET'])
def get_influencer_details(name):
    """Get details for a specific influencer"""
    try:
        data = load_sample_data()
        influencer_data = data[data['influencer_name'] == name]
        
        if influencer_data.empty:
            return jsonify({'status': 'error', 'message': 'Influencer not found'}), 404
        
        cleaned_data = preprocess_data(influencer_data)
        metrics = compute_metrics(cleaned_data)
        credibility = detect_fake_followers(cleaned_data)
        sentiment = analyze_sentiment(cleaned_data)
        
        response = {
            'name': name,
            'metrics': metrics,
            'credibility': credibility,
            'sentiment': sentiment,
            'status': 'success'
        }
        
        return jsonify(response)
    except Exception as e:
        print(f"Error in /api/influencer/{name}: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('modules', exist_ok=True)
    os.makedirs('utils', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    print("=" * 50)
    print("Instagram Influencer Impact Analysis Tool")
    print("=" * 50)
    print(f"Starting Flask application...")
    print(f"Access the dashboard at: http://localhost:5000")
    print("=" * 50)
    print("\nAvailable Routes:")
    print("  /              - Login Page")
    print("  /signup        - Signup Page")
    print("  /dashboard     - Main Dashboard")
    print("  /profile       - User Profile")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Error starting Flask app: {e}")
        sys.exit(1)