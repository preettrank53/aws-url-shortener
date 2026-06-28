import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY', 'default_secret_key_123')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import project modules
from database import init_db, save_url_rds, get_url_rds, increment_clicks_rds, record_click_rds, get_recent_urls_rds, get_all_urls_rds
from dynamodb import get_url_cache, save_url_cache, record_click_analytics
from utils import is_valid_url, generate_short_code

# Initialize the RDS Database tables on startup
try:
    init_db()
except Exception as e:
    logger.error(f"Failed to initialize RDS Database on startup: {e}")

@app.route('/', methods=['GET'])
def index():
    """
    Renders the homepage and lists the 5 most recently shortened URLs.
    """
    recent_urls = []
    try:
        recent_urls = get_recent_urls_rds(limit=5)
    except Exception as e:
        logger.error(f"Error fetching recent URLs for home page: {e}")
        flash("Could not fetch recent URLs due to a database connection issue.", "error")
    
    base_url = os.getenv('BASE_URL', 'http://localhost:5000')
    return render_template('index.html', recent_urls=recent_urls, base_url=base_url)

@app.route('/shorten', methods=['POST'])
def shorten():
    """
    Handles URL shortening requests.
    Validates the original URL, generates a short code, saves to RDS and DynamoDB, and returns the result.
    """
    original_url = request.form.get('original_url', '').strip()
    base_url = os.getenv('BASE_URL', 'http://localhost:5000')
    
    # 1. Validate URL
    if not is_valid_url(original_url):
        logger.warning(f"Invalid URL formatting received: {original_url}")
        flash("Invalid URL format. Please make sure it starts with http:// or https://", "error")
        return redirect(url_for('index'))

    try:
        # 2. Generate unique short code
        max_attempts = 10
        short_code = None
        for _ in range(max_attempts):
            potential_code = generate_short_code()
            # Double check RDS to make sure the code doesn't exist already
            if not get_url_rds(potential_code):
                short_code = potential_code
                break
        
        if not short_code:
            logger.error("Failed to generate a unique short code after maximum attempts.")
            return render_template('error.html', error_title="Generation Error", error_msg="Server failed to generate a unique short code. Please try again.", status_code=500), 500

        # 3. Save to RDS (Permanent storage)
        if save_url_rds(original_url, short_code):
            # 4. Save to DynamoDB cache (Fast lookup)
            save_url_cache(short_code, original_url)
            logger.info(f"Successfully shortened {original_url} to {short_code}")
            
            # Fetch recent URLs to display
            recent_urls = get_recent_urls_rds(limit=5)
            shortened_url = f"{base_url.rstrip('/')}/{short_code}"
            return render_template('index.html', shortened_url=shortened_url, original_url=original_url, recent_urls=recent_urls, base_url=base_url)
        else:
            return render_template('error.html', error_title="Database Error", error_msg="Could not save the URL to our system. Please check your database connection.", status_code=500), 500

    except Exception as e:
        logger.error(f"Unexpected error shortening URL: {e}")
        return render_template('error.html', error_title="Internal Server Error", error_msg="An unexpected error occurred. Please try again later.", status_code=500), 500

@app.route('/<short_code>', methods=['GET'])
def redirect_to_url(short_code):
    """
    Redirects short URLs to their original target.
    Checks DynamoDB cache first, falling back to RDS if there's a cache miss.
    Logs click analytics asynchronously/synchronously to both databases.
    """
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip_address and ',' in ip_address:
        ip_address = ip_address.split(',')[0].strip()
    user_agent = request.headers.get('User-Agent', 'Unknown')
    original_url = None

    try:
        # 1. Check DynamoDB Cache
        original_url = get_url_cache(short_code)
        
        # 2. Check RDS MySQL (Cache Miss)
        if not original_url:
            db_record = get_url_rds(short_code)
            if db_record:
                original_url = db_record['original_url']
                # Restore cache
                save_url_cache(short_code, original_url)
        
        # 3. Redirect if found
        if original_url:
            # Increment click count in RDS (Relational Analytics)
            increment_clicks_rds(short_code)
            # Record detailed click in RDS clicks table
            record_click_rds(short_code, ip_address, user_agent)
            # Record click in DynamoDB click-analytics table (Ultra-fast Writes)
            record_click_analytics(short_code, ip_address, user_agent)
            
            return redirect(original_url)
        
        # 4. Not found anywhere (404)
        return render_template('error.html', error_title="404 Not Found", error_msg="The requested short code does not exist in our system.", status_code=404), 404

    except Exception as e:
        logger.error(f"Error handling redirection for short code {short_code}: {e}")
        return render_template('error.html', error_title="500 Internal Server Error", error_msg="A system database connection error occurred during redirection.", status_code=500), 500

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """
    Renders the URL analytics dashboard.
    """
    try:
        urls = get_all_urls_rds()
        base_url = os.getenv('BASE_URL', 'http://localhost:5000')
        return render_template('dashboard.html', urls=urls, base_url=base_url)
    except Exception as e:
        logger.error(f"Error rendering dashboard: {e}")
        return render_template('error.html', error_title="500 Database Error", error_msg="Failed to load dashboard data. Please verify your database connection.", status_code=500), 500

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_title="404 Page Not Found", error_msg="The page you are looking for does not exist.", status_code=404), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error_title="500 Server Error", error_msg="An internal server error occurred.", status_code=500), 500

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
