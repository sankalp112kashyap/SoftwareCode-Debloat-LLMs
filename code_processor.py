#!/usr/bin/env python3
"""
Code processor for handling Python code files.
"""

import logging
import os
import tokenize
import io

logger = logging.getLogger(__name__)

class CodeProcessor:
    """
    Handles operations related to processing Python code files.
    """
    
    def read_code(self, file_path):
        """
        Read code from a Python file.
        
        Args:
            file_path: Path to the Python file
            
        Returns:
            String containing the Python code
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            raise
    
    def save_code(self, file_path, code):
        """
        Save code to a Python file.
        
        Args:
            file_path: Path to the Python file
            code: The code to save
        """
        # Create a backup of the original file
        backup_path = f"{file_path}.bak"
        try:
            # First make a backup of the original file
            with open(file_path, 'r', encoding='utf-8') as original:
                with open(backup_path, 'w', encoding='utf-8') as backup:
                    backup.write(original.read())
            
            # Then write the new code
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(code)
                
            logger.info(f"Code saved to {file_path} (backup created at {backup_path})")
        except Exception as e:
            logger.error(f"Error saving code to {file_path}: {str(e)}")
            # Try to restore from backup if saving failed
            if os.path.exists(backup_path):
                try:
                    with open(backup_path, 'r', encoding='utf-8') as backup:
                        with open(file_path, 'w', encoding='utf-8') as original:
                            original.write(backup.read())
                    logger.info(f"Restored original file from backup after error")
                except Exception as restore_error:
                    logger.error(f"Failed to restore from backup: {str(restore_error)}")
            raise
      
    def count_lines_of_code(self, code):
        """
        Count all lines of code, including comments and blank lines.
        
        Args:
            code: The Python code as a string
            
        Returns:
            Number of lines in the code
        """
        # Simply count all lines by splitting on newline characters
        return len(code.split('\n'))