from flask import Flask, request, jsonify
from app import detect_language
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# API key from environment variable or default
API_KEY = os.getenv('DETECTLANGUAGE_API_KEY', 'ba3b71e93a655b554f1df2f4b2b1e82b')

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API information"""
    return jsonify({
        "message": "DetectLanguage MCP API",
        "version": "1.0.0",
        "endpoints": {
            "/detect": "POST or GET - Detect language of text",
            "/health": "GET - Health check"
        },
        "usage": {
            "GET": "/detect?text=your_text_here",
            "POST": "Send JSON with 'text' field"
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "detectlanguage-mcp"
    })

@app.route('/detect', methods=['GET', 'POST'])
def detect_text_language():
    """
    Detect language of provided text

    GET: /detect?text=your_text_here
    POST: JSON body with 'text' field
    """
    try:
        # Get text from request
        if request.method == 'GET':
            text = request.args.get('text', '').strip()
        else:  # POST
            if request.is_json:
                data = request.get_json()
                text = data.get('text', '').strip() if data else ''
            else:
                # Handle form data
                text = request.form.get('text', '').strip()

        # Validate input
        if not text:
            return jsonify({
                "success": False,
                "error": "Text parameter is required and cannot be empty",
                "usage": {
                    "GET": "/detect?text=your_text_here",
                    "POST": "Send JSON with 'text' field"
                }
            }), 400

        # Check text length (DetectLanguage API works better with some text)
        if len(text) < 3:
            return jsonify({
                "success": False,
                "error": "Text should be at least 3 characters long for reliable detection",
                "text": text
            }), 400

        # Log the request
        logger.info(f"Language detection request for text: {text[:50]}...")

        # Detect language
        result = detect_language(text, API_KEY)

        # Log the result
        if result.get('success'):
            logger.info(f"Detected language: {result.get('language')} with confidence: {result.get('confidence')}")
        else:
            logger.warning(f"Detection failed: {result.get('error')}")

        # Return result with appropriate status code
        status_code = 200 if result.get('success') else 500

        # Add request info to response
        result['request_method'] = request.method

        # Add timestamp
        from datetime import datetime
        result['timestamp'] = datetime.now().isoformat()

        return jsonify(result), status_code

    except Exception as e:
        logger.error(f"Unexpected error in detect endpoint: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "available_endpoints": {
            "/": "GET - API information",
            "/detect": "GET/POST - Detect language",
            "/health": "GET - Health check"
        }
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        "success": False,
        "error": "Method not allowed for this endpoint"
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.getenv('PORT', 5000))

    # Get host from environment variable or default to localhost
    host = os.getenv('HOST', '0.0.0.0')

    # Get debug mode from environment variable
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

    logger.info(f"Starting DetectLanguage MCP server on {host}:{port}")
    logger.info(f"Debug mode: {debug}")
    logger.info(f"API Key configured: {'Yes' if API_KEY else 'No'}")

    # Start the Flask application
    app.run(
        host=host,
        port=port,
        debug=debug
    )
