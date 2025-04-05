"""
Flask API routes and handlers.
"""

import os

from flask import Flask, jsonify, request

from .browser_utils import extract_headers
from .utils import run_async, read_env_file # type: ignore
from logging_config import main_logger

# Create Flask application
app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health_check():
    """Endpoint to check if the API is running."""
    return jsonify({"status": "healthy", "message": "API is running"}), 200


@app.route("/extract-headers", methods=["GET"])
def extract_booking_headers():
    """Endpoint to trigger header extraction and return the headers."""
    try:
        # Extract headers using the async function
        extractor = run_async(extract_headers())

        if extractor and extractor.headers:
            # Save to .env file if requested
            save_to_file = request.args.get("save", "false").lower() == "true"
            if save_to_file:
                extractor.write_env_variables()

            # Return headers as JSON
            return jsonify(
                {
                    "success": True,
                    "headers": extractor.headers,
                    "saved_to_file": save_to_file,
                }
            ), 200
        else:
            return jsonify(
                {"success": False, "error": "Failed to extract headers"}
            ), 500

    except Exception as e:
        main_logger.error(f"API error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/get-headers", methods=["GET"])
def get_headers():
    """Endpoint to retrieve headers from the .env file."""
    try:
        env_file_path = os.path.join(os.getcwd(), ".env")

        # Check if .env file exists
        if not os.path.exists(env_file_path):
            return jsonify(
                {
                    "success": False,
                    "error": "No headers file found. Try extracting headers first.",
                }
            ), 404

        # Read headers from .env file
        headers = read_env_file()
        
        if not headers:
            return jsonify(
                {
                    "success": False,
                    "error": "Error reading headers from file.",
                }
            ), 500

        return jsonify({"success": True, "headers": headers}), 200

    except Exception as e:
        main_logger.error(f"API error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500