#!/usr/bin/env python3
"""
Configuration settings for the LLM code debloat project.
"""

import os
import json
import logging

logger = logging.getLogger(__name__)

# Default prompts for each LLM
DEFAULT_PROMPT = """
Goal*
You are an experienced software engineer. Please debloat the code in this file while maintaining its functional correctness. Simplify logic, remove redundancies, and optimize for readability and maintainability without introducing new bugs.

IMPORTANT 
1.⁠ ⁠All rewritten code must remain within the file it originated from.  
2.⁠ ⁠No new files or services may be introduced as part of the solution.  
3.⁠ ⁠Adding helper methods within the file is allowed but must not break functional correctness.  
4.⁠ ⁠Do not modify OR remove comments, as they do not count as code.  Imports also do not count as code.

Context
Software bloat refers to unnecessary or inefficient CODE that increases a program’s size or reduces its performance without contributing meaningful functionality.
"""

# Model configurations
MODEL_CONFIGS = {
    "claude-3-5-sonnet": {
        "api_key_env": "ANTHROPIC_API_KEY",
        "model_id": "claude-3-5-sonnet-20241022",
        "max_tokens": 4000,
        "temperature": 0.1
    },
    "gemini-2-0-flash": {
        "api_key_env": "GOOGLE_API_KEY",
        "model_id": "gemini-1.5-flash",
        "max_tokens": 4000,
        "temperature": 0.1
    },
    "gpt-4o": {
        "api_key_env": "OPENAI_API_KEY",
        "model_id": "gpt-4o",
        "max_tokens": 4000,
        "temperature": 0.1
    },
    "deepseek-r1": {
        "api_key_env": "DEEPSEEK_API_KEY",
        "model_id": "deepseek-code-r1",
        "max_tokens": 4000,
        "temperature": 0.1
    }
}

def get_model_config(model_name):
    """
    Get the configuration for a specific model.
    
    Args:
        model_name: Name of the model
        
    Returns:
        Dictionary with model configuration
    """
    if model_name not in MODEL_CONFIGS:
        logger.error(f"Unknown model: {model_name}")
        raise ValueError(f"Unknown model: {model_name}")
    
    return MODEL_CONFIGS[model_name]

def save_config(config_path="config.json"):
    """
    Save the current configuration to a JSON file.
    
    Args:
        config_path: Path to save the configuration
    """
    try:
        config = {
            "default_prompt": DEFAULT_PROMPT,
            "models": MODEL_CONFIGS
        }
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
            
        logger.info(f"Configuration saved to {config_path}")
    except Exception as e:
        logger.error(f"Error saving configuration: {str(e)}")

def load_config(config_path="config.json"):
    """
    Load configuration from a JSON file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Configuration dictionary
    """
    global DEFAULT_PROMPT, MODEL_CONFIGS
    
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                
            if "default_prompt" in config:
                DEFAULT_PROMPT = config["default_prompt"]
                
            if "models" in config:
                MODEL_CONFIGS = config["models"]
                
            logger.info(f"Configuration loaded from {config_path}")
            return config
        else:
            logger.warning(f"Configuration file not found: {config_path}")
            return {"default_prompt": DEFAULT_PROMPT, "models": MODEL_CONFIGS}
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        return {"default_prompt": DEFAULT_PROMPT, "models": MODEL_CONFIGS}