#!/usr/bin/env python3
"""
Visualization tools for LLM code debloat results.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import logging
import argparse
from datetime import datetime

logger = logging.getLogger(__name__)

class ResultsVisualizer:
    """
    Visualizes results from the bloat removal Excel file.
    """
    
    def __init__(self, excel_path):
        """
        Initialize the visualizer.
        
        Args:
            excel_path: Path to the Excel file with results
        """
        self.excel_path = excel_path
        self.data = None
        self._load_data()
    
    def _load_data(self):
        """Load data from the Excel file."""
        try:
            if not os.path.exists(self.excel_path):
                logger.error(f"Results file not found: {self.excel_path}")
                return
            
            self.data = pd.read_excel(self.excel_path)
            logger.info(f"Loaded {len(self.data)} records from {self.excel_path}")
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
    
    def plot_loc_reduction(self, output_path=None):
        """
        Plot lines of code reduction by LLM model.
        
        Args:
            output_path: Path to save the plot, or None to display it
        """
        if self.data is None or len(self.data) == 0:
            logger.error("No data available for plotting")
            return
        
        try:
            # Group by LLM model and calculate mean LOC reduction
            loc_reduction_by_model = self.data.groupby('LLM Model')['LOC Reduction (%)'].mean().sort_values(ascending=False)
            
            plt.figure(figsize=(10, 6))
            bars = plt.bar(loc_reduction_by_model.index, loc_reduction_by_model.values, color='skyblue')
            
            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'{height:.1f}%', ha='center', va='bottom')
            
            plt.title('Average Lines of Code Reduction by LLM Model')
            plt.ylabel('LOC Reduction (%)')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            
            if output_path:
                plt.savefig(output_path)
                logger.info(f"LOC reduction plot saved to {output_path}")
            else:
                plt.show()
        except Exception as e:
            logger.error(f"Error plotting LOC reduction: {str(e)}")
    
    def generate_summary_report(self, output_path=None):
        """
        Generate a summary report of the results.
        
        Args:
            output_path: Path to save the report, or None to display it
        """
        if self.data is None or len(self.data) == 0:
            logger.error("No data available for report")
            return
        
        try:
            # Create a summary grouped by LLM model
            summary = self.data.groupby('LLM Model').agg({
                'File Name': 'count',
                'LOC Reduction (%)': 'mean'
            }).reset_index()
            
            # Rename and reorder columns
            summary = summary.rename(columns={'File Name': 'Files Processed'})
            summary = summary[[
                'LLM Model', 'Files Processed', 
                'LOC Reduction (%)'
            ]]
            
            # Round numeric columns
            for col in summary.columns:
                if col != 'LLM Model' and col != 'Files Processed':
                    summary[col] = summary[col].round(2)
            
            # Calculate overall statistics
            overall = pd.DataFrame({
                'LLM Model': ['OVERALL'],
                'Files Processed': [len(self.data)],
                'LOC Reduction (%)': [self.data['LOC Reduction (%)'].mean()]
            })
            
            # Round overall statistics
            for col in overall.columns:
                if col != 'LLM Model' and col != 'Files Processed':
                    overall[col] = overall[col].round(2)
            
            # Combine summary and overall
            report = pd.concat([summary, overall], ignore_index=True)
            
            if output_path:
                # Save to CSV
                report.to_csv(output_path, index=False)
                logger.info(f"Summary report saved to {output_path}")
                
                # Also print to console
                print("\nSummary Report:")
                print(report.to_string(index=False))
            else:
                # Print to console
                print("\nSummary Report:")
                print(report.to_string(index=False))
        except Exception as e:
            logger.error(f"Error generating summary report: {str(e)}")
    
    def generate_full_report(self, output_dir=None):
        """
        Generate a full report with plots and summary.
        
        Args:
            output_dir: Directory to save the report, or None to display it
        """
        if self.data is None or len(self.data) == 0:
            logger.error("No data available for report")
            return
        
        try:
            # Create output directory if it doesn't exist
            if output_dir:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                report_dir = os.path.join(output_dir, f"debloat_report_{timestamp}")
                os.makedirs(report_dir, exist_ok=True)
                
                # Generate plots
                self.plot_loc_reduction(os.path.join(report_dir, "loc_reduction.png"))
                
                # Generate summary report
                self.generate_summary_report(os.path.join(report_dir, "summary_report.csv"))
                
                # Save the raw data
                self.data.to_excel(os.path.join(report_dir, "raw_data.xlsx"), index=False)
                
                logger.info(f"Full report generated in {report_dir}")
            else:
                # Display plots
                self.plot_loc_reduction()
                
                # Generate summary report
                self.generate_summary_report()
        except Exception as e:
            logger.error(f"Error generating full report: {str(e)}")

def main():
    """Main function to visualize bloat removal results."""
    parser = argparse.ArgumentParser(description='Visualize bloat removal results.')
    parser.add_argument('--excel', type=str, required=True, help='Path to the Excel file with results')
    parser.add_argument('--output_dir', type=str, help='Directory to save the report')
    parser.add_argument('--plot_type', type=str, choices=['loc', 'all'],
                      help='Type of plot to generate')
    parser.add_argument('--summary', action='store_true', help='Generate a summary report')
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("visualization.log"),
            logging.StreamHandler()
        ]
    )
    
    visualizer = ResultsVisualizer(args.excel)
    
    if args.plot_type == 'loc':
        visualizer.plot_loc_reduction(args.output_dir + '/loc_reduction.png' if args.output_dir else None)
    elif args.plot_type == 'all':
        if args.output_dir:
            visualizer.generate_full_report(args.output_dir)
        else:
            visualizer.plot_loc_reduction()
    
    if args.summary:
        visualizer.generate_summary_report(args.output_dir + '/summary_report.csv' if args.output_dir else None)
    
    # If no specific action is specified, generate a full report
    if not args.plot_type and not args.summary:
        visualizer.generate_full_report(args.output_dir)

if __name__ == '__main__':
    main()