"""
Main entry point for the application.
"""

from components.api import app

if __name__ == "__main__":
    # Run the Flask app
    app.run(host="0.0.0.0", port=4000, debug=False)