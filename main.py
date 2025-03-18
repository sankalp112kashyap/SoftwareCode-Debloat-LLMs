#!/usr/bin/env python3
"""
Main script for automating software bloat detection and removal using LLMs.
"""

import argparse
import os
import logging
from llm_handler import LLMHandler
from code_processor import CodeProcessor
from metrics_recorder import MetricsRecorder
from utils import load_environment_variables, normalize_file_path
from config import load_config
from prompts import PROMPTS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bloat_removal.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def process_file(code_file, llm_model, output_excel, args, export_path=None, prompt=None):
    """Process a single file for bloat removal."""
    try:
        # Initialize components
        code_processor = CodeProcessor()
        llm_handler = LLMHandler()
        metrics_recorder = MetricsRecorder(output_excel)
        
        logger.info(f"Starting bloat removal process for {code_file} using {llm_model}")
        
        # Step 1: Read original code
        original_code = code_processor.read_code(code_file)
        original_loc = code_processor.count_lines_of_code(original_code)
        logger.info(f"Original code has {original_loc} lines")
        
        # Step 2: Send code to LLM for optimization
        optimized_code = llm_handler.optimize_code(llm_model, original_code, prompt or PROMPTS["1"])
        optimized_loc = code_processor.count_lines_of_code(optimized_code)
        logger.info(f"Optimized code has {optimized_loc} lines")
        
        # Step 3: Save optimized code
        save_path = export_path if export_path else code_file
        code_processor.save_code(save_path, optimized_code)
        logger.info(f"Optimized code saved to {save_path}")
        
        # Step 4: Calculate metrics
        loc_reduction_percentage = ((original_loc - optimized_loc) / original_loc) * 100 if original_loc > 0 else 0
        
        # Get full prompt text for metrics
        prompt_text = prompt if args.custom_prompt else PROMPTS[args.prompt if args.prompt else '1']
        
        # Step 5: Record results
        metrics_recorder.record_metrics(
            file_name=code_file,
            llm_model=llm_model,
            loc_before=original_loc,
            loc_after=optimized_loc,
            loc_reduction_percentage=loc_reduction_percentage,
            prompt_text=prompt_text
        )

        # Check results
        if original_code == optimized_code:
            logger.warning("LLM did not make any changes to the code")
        elif len(original_code.split('\n')) == len(optimized_code.split('\n')):
            logger.warning("LLM made changes but didn't reduce line count")
        
        logger.info(f"Results recorded in {output_excel}")
        return True
    except Exception as e:
        logger.error(f"An error occurred during processing: {str(e)}", exc_info=True)
        return False

def main():
    """Main function to execute the software bloat removal process."""
    # Load environment variables and configuration
    load_environment_variables()
    load_config()
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Identify and remove software bloat using LLMs.')
    parser.add_argument('--code_file', type=str, required=True, 
                       help='Path to the Python file with bloated code')
    parser.add_argument('--llm_model', type=str, required=True, 
                       choices=['claude-3-5-sonnet', 'gemini-2-0-flash', 'gpt-4o', 'deepseek-r1'],
                       help='LLM model to use for code optimization')
    parser.add_argument('--output_excel', type=str, default='bloat_removal_results.xlsx',
                       help='Path to output Excel file (default: bloat_removal_results.xlsx)')
    parser.add_argument('--prompt', type=str, choices=list(PROMPTS.keys()),
                       help='Choose the prompt type for code optimization (default: 1)')
    parser.add_argument('--custom_prompt', type=str, 
                       help='Custom prompt to use instead of predefined prompts')
    parser.add_argument('--export_path', type=str,
                       help='Path to export the optimized code (if not specified, original file is updated)')
    
    args = parser.parse_args()
    
    # Select prompt
    selected_prompt = args.custom_prompt if args.custom_prompt else PROMPTS[args.prompt if args.prompt else "1"]
    logger.info(f"Using prompt: {args.prompt if args.prompt else '1' if not args.custom_prompt else 'custom'}")
    
    # Normalize file paths
    code_file = normalize_file_path(args.code_file)
    export_path = normalize_file_path(args.export_path) if args.export_path else None
    
    # Validate input files
    if not os.path.isfile(code_file):
        logger.error(f"Code file not found: {code_file}")
        return
    
    # Process the file with selected prompt
    success = process_file(code_file, args.llm_model, args.output_excel, args, export_path, 
                         prompt=selected_prompt)
    
    if success:
        logger.info("Bloat removal process completed successfully")
    else:
        logger.error("Bloat removal process failed")

if __name__ == "__main__":
    main()

