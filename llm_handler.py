#!/usr/bin/env python3
"""
LLM handler for interacting with different LLM APIs.
"""

import os
import logging
import anthropic
import google.generativeai as genai
from openai import OpenAI
import requests
import time

logger = logging.getLogger(__name__)

class LLMHandler:
    """
    Handles interactions with different LLM APIs for code optimization.
    """
    
    def __init__(self):
        """Initialize the LLM handler with API keys from environment variables."""
        # Load API keys from environment variables
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        
        # Initialize API clients
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize API clients for different LLMs."""
        # Initialize clients only if API keys are available
        self.clients = {}
        
        if self.anthropic_api_key:
            self.clients['claude'] = anthropic.Anthropic(
                api_key=self.anthropic_api_key
            )
        
        if self.openai_api_key:
            self.clients['openai'] = OpenAI(
                api_key=self.openai_api_key
            )
        
        if self.google_api_key:
            genai.configure(api_key=self.google_api_key)
            self.clients['gemini'] = genai
    
    def optimize_code(self, model_name, code, prompt):
        """
        Send code to the specified LLM for optimization.
        
        Args:
            model_name: Name of the LLM model to use (claude-3-7-sonnet, gemini-2-0-flash, gpt-4o, deepseek-r1)
            code: The code to optimize
            prompt: The prompt to send to the LLM
            
        Returns:
            Optimized code from the LLM
        """
        full_prompt = f"{prompt}\n\n```python\n{code}\n```"
        
        try:
            if model_name == 'claude-3-7-sonnet':
                return self._call_claude(full_prompt)
            elif model_name == 'gemini-2-0-flash':
                return self._call_gemini(full_prompt)
            elif model_name == 'gpt-4o':
                return self._call_openai(full_prompt)
            elif model_name == 'deepseek-r1':
                return self._call_deepseek(full_prompt)
            else:
                raise ValueError(f"Unsupported model: {model_name}")
        except Exception as e:
            logger.error(f"Error calling {model_name}: {str(e)}", exc_info=True)
            # Return original code if API call fails
            return code
    
    def _call_claude(self, prompt):
        """Call Claude API to optimize code."""
        if 'claude' not in self.clients:
            raise ValueError("Claude API key not found in environment variables")
        
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                # Use the correct model name as shown in your screenshot
                response = self.clients['claude'].messages.create(
                    model="claude-3-7-sonnet-20250219",  # Updated to match your screenshot
                    max_tokens=4000,
                    temperature=0.1,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return self._extract_code_from_response(response.content[0].text)
            except Exception as e:
                logger.error(f"Error calling Claude API (attempt {attempt+1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    # Wait before retrying, with exponential backoff
                    sleep_time = retry_delay * (2 ** attempt)
                    logger.info(f"Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    raise
                
    def _call_gemini(self, prompt):
        """Call Gemini API to optimize code."""
        if 'gemini' not in self.clients:
            raise ValueError("Google API key not found in environment variables")
        
        try:
            model = self.clients['gemini'].GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            return self._extract_code_from_response(response.text)
        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            raise
    
    def _call_openai(self, prompt):
        """Call OpenAI API to optimize code."""
        if 'openai' not in self.clients:
            raise ValueError("OpenAI API key not found in environment variables")
        
        try:
            response = self.clients['openai'].chat.completions.create(
                model="gpt-4o",
                temperature=0.1,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return self._extract_code_from_response(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}")
            raise
    
    def _call_deepseek(self, prompt):
        """Call DeepSeek API to optimize code."""
        if not self.deepseek_api_key:
            raise ValueError("DeepSeek API key not found in environment variables")
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.deepseek_api_key}"
            }
            
            payload = {
                "model": "deepseek-code-r1",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 4000
            }
            
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            response.raise_for_status()
            response_json = response.json()
            return self._extract_code_from_response(response_json['choices'][0]['message']['content'])
        except Exception as e:
            logger.error(f"Error calling DeepSeek API: {str(e)}")
            raise
    
    def _extract_code_from_response(self, response_text):
        """Extract code from LLM response."""
        # Look for code between Python code blocks
        code_blocks = response_text.split("```python")
        if len(code_blocks) > 1:
            code_part = code_blocks[1].split("```")[0]
            return code_part.strip()
        
        # Look for code between generic code blocks
        code_blocks = response_text.split("```")
        if len(code_blocks) > 1:
            # If we have multiple code blocks, take the longest one
            code_candidates = [block for i, block in enumerate(code_blocks) if i % 2 == 1]
            if code_candidates:
                return max(code_candidates, key=len).strip()
        
        # If no code blocks are found, return the entire response
        logger.warning("No code blocks found in LLM response, returning full response.")
        return response_text