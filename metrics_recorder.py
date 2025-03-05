#!/usr/bin/env python3
"""
Metrics recorder for saving results to Excel.
"""

import os
import logging
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)

class MetricsRecorder:
    """
    Records metrics from bloat removal experiments to an Excel file.
    """
    
    def __init__(self, excel_path):
        """
        Initialize the metrics recorder.
        
        Args:
            excel_path: Path to the Excel file
        """
        self.excel_path = excel_path
        self.ensure_excel_exists()
    
    def ensure_excel_exists(self):
        """Ensure that the Excel file exists with the proper columns."""
        try:
            if os.path.exists(self.excel_path):
                # File exists, check if it has the right structure
                try:
                    df = pd.read_excel(self.excel_path)
                    # Check if it has all required columns
                    required_columns = [
                        'Timestamp', 'File Name', 'LLM Model',
                        'LOC Before', 'LOC After', 'LOC Reduction (%)'
                    ]
                    
                    if not all(col in df.columns for col in required_columns):
                        # Missing columns, create a new file
                        self._create_new_excel()
                except Exception:
                    # Could not read the file or it has wrong format, create a new one
                    self._create_new_excel()
            else:
                # File does not exist, create it
                self._create_new_excel()
        except Exception as e:
            logger.error(f"Error ensuring Excel file exists: {str(e)}")
            raise
    
    def _create_new_excel(self):
        """Create a new Excel file with the correct columns."""
        try:
            # Create a DataFrame with the correct columns
            df = pd.DataFrame(columns=[
                'Timestamp', 'File Name', 'LLM Model',
                'LOC Before', 'LOC After', 'LOC Reduction (%)'
            ])
            
            # Save to Excel
            df.to_excel(self.excel_path, index=False)
            logger.info(f"Created new Excel file at {self.excel_path}")
        except Exception as e:
            logger.error(f"Error creating Excel file: {str(e)}")
            raise
    
    def record_metrics(self, file_name, llm_model, 
                      loc_before, loc_after, loc_reduction_percentage):
        """
        Record metrics to the Excel file.
        
        Args:
            file_name: Name of the file being optimized
            llm_model: Name of the LLM model used
            loc_before: Lines of code before optimization
            loc_after: Lines of code after optimization
            loc_reduction_percentage: Percentage reduction in lines of code
        """
        try:
            # Create a new data row
            new_row = {
                'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'File Name': os.path.basename(file_name),
                'LLM Model': llm_model,
                'LOC Before': loc_before,
                'LOC After': loc_after,
                'LOC Reduction (%)': round(loc_reduction_percentage, 2)
            }
            
            # Read existing Excel file
            if os.path.exists(self.excel_path):
                df = pd.read_excel(self.excel_path)
            else:
                # If file doesn't exist, create a new DataFrame
                df = pd.DataFrame(columns=list(new_row.keys()))
            
            # Append the new row
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            
            # Save to Excel
            df.to_excel(self.excel_path, index=False)
            logger.info(f"Metrics recorded to {self.excel_path}")
        except Exception as e:
            logger.error(f"Error recording metrics: {str(e)}")
            raise