"""
Fynd AI Intern - Task 2 Backend
Flask API for managing reviews and AI-generated responses
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import csv
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
import uuid

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Data file paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)
REVIEWS_FILE = os.path.join(DATA_DIR, 'reviews.json')

# Initialize data file if it doesn't exist
if not os.path.exists(REVIEWS_FILE):
    with open(REVIEWS_FILE, 'w') as f:
        json.dump([], f)


def _choose_fallback_model() -> str:
    """Choose a supported model if the configured one fails."""
    # Prefer newer, widely available models; fallback to legacy.
    candidates = [
        'gemini-2.5-flash',
        'gemini-2.5-pro',
        'gemini-2.0-flash',
        'gemini-1.5-pro',
        'gemini-pro',
    ]
    return candidates[0]


def call_gemini(prompt: str) -> str:
    """Call Gemini API"""
    try:
        # Use a current model; allow override via env
        model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Fallback when the selected model is unavailable (e.g., model not found)
        if 'not found' in str(e).lower() or '404' in str(e):
            try:
                fallback_model = _choose_fallback_model()
                model = genai.GenerativeModel(fallback_model)
                response = model.generate_content(prompt)
                return response.text
            except Exception:
                pass
        print(f"Error calling Gemini API: {e}")
        return f"Error: {str(e)}"


def generate_ai_response(review: str, rating: int) -> str:
    """Generate AI response to user review"""
    prompt = f"""You are a helpful customer service representative. A customer left this review:

Rating: {rating}/5 stars
Review: {review}

Provide a brief, empathetic response (2-3 sentences) thanking them for the review and addressing their feedback appropriately."""
    
    return call_gemini(prompt)


def generate_summary(review: str) -> str:
    """Generate summary of the review"""
    prompt = f"""Provide a brief 1-sentence summary of this review:
{review}

Summary:"""
    
    return call_gemini(prompt).strip()


def generate_recommended_actions(review: str, rating: int) -> str:
    """Generate recommended actions based on the review"""
    prompt = f"""Based on this review, suggest ONE specific action the business should take to improve:

Rating: {rating}/5 stars
Review: {review}

Recommendation:"""
    
    return call_gemini(prompt).strip()


@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    """Get all reviews"""
    try:
        if os.path.exists(REVIEWS_FILE):
            with open(REVIEWS_FILE, 'r') as f:
                reviews = json.load(f)
                return jsonify(reviews)
        return jsonify([])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reviews', methods=['POST'])
def create_review():
    """Create a new review with AI-generated response"""
    try:
        data = request.json
        review_text = data.get('review')
        rating = int(data.get('rating', 3))
        
        # Validate input
        if not review_text or not review_text.strip():
            return jsonify({'error': 'Review text is required'}), 400
        
        if not 1 <= rating <= 5:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        # Generate AI content
        ai_response = generate_ai_response(review_text, rating)
        summary = generate_summary(review_text)
        recommendations = generate_recommended_actions(review_text, rating)
        
        # Create review object
        review_obj = {
            'id': str(uuid.uuid4()),
            'rating': rating,
            'review': review_text,
            'ai_response': ai_response,
            'summary': summary,
            'recommended_action': recommendations,
            'timestamp': datetime.now().isoformat()
        }
        
        # Load existing reviews
        with open(REVIEWS_FILE, 'r') as f:
            reviews = json.load(f)
        
        # Add new review
        reviews.append(review_obj)
        
        # Save updated reviews
        with open(REVIEWS_FILE, 'w') as f:
            json.dump(reviews, f, indent=2)
        
        return jsonify(review_obj), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """Get a specific review"""
    try:
        with open(REVIEWS_FILE, 'r') as f:
            reviews = json.load(f)
        
        for review in reviews:
            if review['id'] == review_id:
                return jsonify(review)
        
        return jsonify({'error': 'Review not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete a review"""
    try:
        with open(REVIEWS_FILE, 'r') as f:
            reviews = json.load(f)
        
        reviews = [r for r in reviews if r['id'] != review_id]
        
        with open(REVIEWS_FILE, 'w') as f:
            json.dump(reviews, f, indent=2)
        
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics about reviews"""
    try:
        with open(REVIEWS_FILE, 'r') as f:
            reviews = json.load(f)
        
        if not reviews:
            return jsonify({
                'total_reviews': 0,
                'average_rating': 0,
                'rating_distribution': {}
            })
        
        total_reviews = len(reviews)
        average_rating = sum(r['rating'] for r in reviews) / total_reviews
        
        rating_distribution = {}
        for i in range(1, 6):
            rating_distribution[str(i)] = sum(1 for r in reviews if r['rating'] == i)
        
        return jsonify({
            'total_reviews': total_reviews,
            'average_rating': round(average_rating, 2),
            'rating_distribution': rating_distribution
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


# Serve frontend files
@app.route('/')
@app.route('/user')
def user_dashboard():
    """Serve user dashboard"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/admin')
def admin_dashboard():
    """Serve admin dashboard"""
    return send_from_directory(app.static_folder, 'admin.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
