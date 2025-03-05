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
As an expert software engineer and debugger, identify and remove bloat from the code 
so that program size is less and if possible code becomes more efficient. Make sure 
while doing this, the code's functionality correctness is preserved. It should not 
make changes in the code that makes it lose its functional correctness. Also, make 
sure that you don't remove important comments while debloating code.
"""

# Model configurations
MODEL_CONFIGS = {
    "claude-3-7-sonnet": {
        "api_key_env": "ANTHROPIC_API_KEY",
        "model_id": "claude-3-7-sonnet-20240229",
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