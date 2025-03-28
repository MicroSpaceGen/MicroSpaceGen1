"""
Utility Functions Module
Common helper functions used throughout the project.
"""

import os
import json
from typing import Dict, Any, Optional
from datetime import datetime
import logging

def setup_logging(log_level: str = "INFO") -> None:
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load config: {str(e)}")
        raise

def save_data(data: Dict[str, Any], filepath: str) -> bool:
    """Save data to JSON file"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        logging.error(f"Failed to save data: {str(e)}")
        return False

def load_data(filepath: str) -> Optional[Dict[str, Any]]:
    """Load data from JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load data: {str(e)}")
        return None

def generate_timestamp() -> str:
    """Generate ISO format timestamp"""
    return datetime.now().isoformat()

def validate_data(data: Dict[str, Any], required_fields: list) -> bool:
    """Validate data contains required fields"""
    return all(field in data for field in required_fields) 