#!/usr/bin/env python3
"""
Batch processor for processing multiple files.
"""

import os
import logging
import argparse
import csv
import time
from main import process_file
from utils import normalize_file_path

logger = logging.getLogger(__name__)

def process_batch_from_csv(csv_file, llm_model, output_excel, export_dir=None):
    """
    Process a batch of files specified in a CSV file.
    
    Args:
        csv_file: Path to CSV file with code file paths
        llm_model: LLM model to use
        output_excel: Path to output Excel file
        export_dir: Directory to export optimized code (if None, original files are updated)
    """
    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            if 'code_file' not in reader.fieldnames:
                logger.error("CSV file must contain 'code_file' column")
                return
            
            for row in reader:
                code_file = normalize_file_path(row['code_file'])
                
                if not os.path.exists(code_file):
                    logger.error(f"Code file not found: {code_file}")
                    continue
                
                # Determine export path if export_dir is specified
                export_path = None
                if export_dir:
                    export_path = os.path.join(export_dir, os.path.basename(code_file))
                
                logger.info(f"Processing {code_file}")
                try:
                    process_file(code_file, llm_model, output_excel, export_path)
                    # Add a small delay between API calls to avoid rate limits
                    time.sleep(2)
                except Exception as e:
                    logger.error(f"Error processing {code_file}: {str(e)}")
    except Exception as e:
        logger.error(f"Error processing batch from CSV: {str(e)}")

def create_batch_csv_template(output_path):
    """
    Create a template CSV file for batch processing.
    
    Args:
        output_path: Path to save the CSV template
    """
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['code_file'])
            writer.writerow(['path/to/code1.py'])
            writer.writerow(['path/to/code2.py'])
        
        logger.info(f"CSV template created at {output_path}")
    except Exception as e:
        logger.error(f"Error creating CSV template: {str(e)}")

def main():
    """Main function for batch processing."""
    parser = argparse.ArgumentParser(description='Process a batch of files for bloat removal.')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Create template command
    template_parser = subparsers.add_parser('create-template', help='Create a CSV template')
    template_parser.add_argument('--output', type=str, default='batch_files.csv', 
                                help='Path to save the CSV template')
    
    # Process batch command
    batch_parser = subparsers.add_parser('process', help='Process a batch of files')
    batch_parser.add_argument('--csv', type=str, required=True, 
                             help='Path to CSV file with code file paths')
    batch_parser.add_argument('--llm_model', type=str, required=True,
                            choices=['claude-3-7-sonnet', 'gemini-2-0-flash', 'gpt-4o', 'deepseek-r1'],
                            help='LLM model to use')
    batch_parser.add_argument('--output_excel', type=str, default='bloat_removal_results.xlsx',
                            help='Path to output Excel file')
    batch_parser.add_argument('--export_dir', type=str,
                            help='Directory to export optimized code (if not specified, original files are updated)')
    
    args = parser.parse_args()
    
    if args.command == 'create-template':
        create_batch_csv_template(args.output)
    elif args.command == 'process':
        process_batch_from_csv(args.csv, args.llm_model, args.output_excel, args.export_dir)
    else:
        parser.print_help()

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("batch_processing.log"),
            logging.StreamHandler()
        ]
    )
    
    main()