#!/usr/bin/env python3
"""
Utility functions for the LLM code debloat project.
"""

import os
import logging
import dotenv

logger = logging.getLogger(__name__)

def load_environment_variables():
    """
    Load environment variables from .env file.
    """
    try:
        # Try to load from .env file if it exists
        dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
        if os.path.exists(dotenv_path):
            dotenv.load_dotenv(dotenv_path)
            logger.info(f"Loaded environment variables from {dotenv_path}")
            
            # Check if the required API keys are available
            required_api_keys = {
                'claude-3-7-sonnet': 'ANTHROPIC_API_KEY',
                'gpt-4o': 'OPENAI_API_KEY',
                'gemini-2-0-flash': 'GOOGLE_API_KEY',
                'deepseek-r1': 'DEEPSEEK_API_KEY'
            }
            
            available_models = []
            for model, env_var in required_api_keys.items():
                if os.getenv(env_var):
                    available_models.append(model)
            
            if available_models:
                logger.info(f"Available LLM models: {', '.join(available_models)}")
            else:
                logger.warning("No API keys found. Please set the required API keys in the .env file.")
        else:
            logger.warning(f".env file not found at {dotenv_path}. Using environment variables from system.")
    except Exception as e:
        logger.error(f"Error loading environment variables: {str(e)}")

def normalize_file_path(file_path):
    """
    Normalize a file path to an absolute path.
    
    Args:
        file_path: Path to normalize
        
    Returns:
        Absolute path
    """
    if os.path.isabs(file_path):
        return file_path
    return os.path.abspath(os.path.join(os.getcwd(), file_path))

def create_backup_directory():
    """
    Create a backup directory for storing original code files.
    
    Returns:
        Path to the backup directory
    """
    backup_dir = os.path.join(os.getcwd(), "code_backups")
    if not os.path.exists(backup_dir):
        try:
            os.makedirs(backup_dir)
            logger.info(f"Created backup directory at {backup_dir}")
        except Exception as e:
            logger.error(f"Error creating backup directory: {str(e)}")
            backup_dir = os.getcwd()  # Fallback to current directory
    
    return backup_dir