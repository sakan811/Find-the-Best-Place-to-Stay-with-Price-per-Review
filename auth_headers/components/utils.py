"""
Utility functions for the application.
"""

import asyncio
import os
from typing import Dict

from logging_config import main_logger


def run_async(func):  # type: ignore
    """Run an async function in a synchronous context."""
    try:
        # Try to get the existing event loop
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # If no event loop exists, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(func)  # type: ignore


def read_env_file() -> Dict[str, str]:
    """Read environment variables from .env file."""
    env_file_path = os.path.join(os.getcwd(), ".env")
    
    # Check if .env file exists
    if not os.path.exists(env_file_path):
        main_logger.warning("No .env file found.")
        return {}
        
    headers: Dict[str, str] = {}
    try:
        with open(env_file_path, "r") as file:
            for line in file:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    # Remove surrounding quotes if present
                    value = value.strip("\"'")
                    headers[key] = value
        return headers
    except Exception as e:
        main_logger.error(f"Error reading .env file: {e}")
        return {}