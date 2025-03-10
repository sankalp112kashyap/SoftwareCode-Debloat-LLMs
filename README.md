# LLM Code Debloat

A tool for identifying and removing software bloat using Large Language Models (LLMs). This project is part of a research study at UC Davis evaluating the effectiveness of different LLMs in identifying and removing software bloat while maintaining code functionality.

## Project Overview

Software bloat refers to unnecessary or inefficient code that increases a program's size or reduces its performance without contributing meaningful functionality. This tool automates the process of:

1. Taking a Python file with potentially bloated code
2. Sending the code to an LLM (Claude, GPT-4o, Gemini, or DeepSeek) with a prompt to identify and remove bloat
3. Saving the optimized code (either replacing the original or to a new file)
4. Recording metrics such as lines of code reduction in an Excel file

## Features

- Support for multiple LLM APIs:
  - Claude 3.7 Sonnet (Anthropic)
  - GPT-4o (OpenAI)
  - Gemini 2.0 Flash (Google)
  - DeepSeek R1
- Comprehensive metrics collection:
  - Lines of code before and after optimization
  - Percentage reduction in lines of code
- Batch processing of multiple files
- Option to export optimized code to a separate file instead of replacing the original
- Automatic backup of original code files
- Visualization of results with charts

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/llm-code-debloat.git
   cd llm-code-debloat
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your API keys:
   ```bash
   cp .env.example .env
   ```
   Then edit the `.env` file with your actual API keys.

## Usage

### Single File Processing

To process a single Python file:

```bash
python main.py --code_file path/to/bloated_code.py --llm_model claude-3-7-sonnet
```

To specify which prompt to use (default is prompt "1"):

```bash
python main.py --code_file path/to/bloated_code.py --llm_model claude-3-7-sonnet --prompt 1
```

To use a custom prompt:

```bash
python main.py --code_file path/to/bloated_code.py --llm_model claude-3-7-sonnet --custom_prompt "Your custom prompt here"
```

To export the optimized code to a different file instead of replacing the original:

```bash
python main.py --code_file path/to/bloated_code.py --llm_model claude-3-7-sonnet --export_path path/to/optimized_code.py
```

Available options for `--llm_model`:
- `claude-3-7-sonnet` (Anthropic)
- `gpt-4o` (OpenAI)
- `gemini-2-0-flash` (Google)
- `deepseek-r1` (DeepSeek)

### Batch Processing

For processing multiple files at once:

1. Create a CSV template:
   ```bash
   python batch_processor.py create-template --output files_to_process.csv
   ```

2. Edit the CSV file with your code file paths.

3. Process all files in the CSV:
   ```bash
   python batch_processor.py process --csv files_to_process.csv --llm_model gpt-4o
   ```

4. To export optimized code to a separate directory instead of replacing the originals:
   ```bash
   python batch_processor.py process --csv files_to_process.csv --llm_model gpt-4o --export_dir optimized_code/
   ```

### Available Prompts

The tool comes with predefined prompts that can be selected using the `--prompt` flag:

- `1` (Default): Comprehensive prompt focused on maintaining functional correctness while removing bloat
- `2`: Minimal prompt for basic debloating

Full descriptions of each prompt:

#### Prompt 1
```
Goal*
You are an experienced software engineer. Please debloat the code in this file while maintaining its functional correctness. Simplify logic, remove redundancies, and optimize for readability and maintainability without introducing new bugs.

IMPORTANT 
1. All rewritten code must remain within the file it originated from.  
2. No new files or services may be introduced as part of the solution.  
3. Adding helper methods within the file is allowed but must not break functional correctness.  
4. Do not modify OR remove comments, as they do not count as code.  Imports also do not count as code.

Context
Software bloat refers to unnecessary or inefficient CODE that increases a program's size or reduces its performance without contributing meaningful functionality.
```

#### Prompt 2
```
Debloat this file while maintaining functional correctness
```

## Project Structure

```
llm-code-debloat/
├── main.py                    # Main script for processing single files
├── llm_handler.py             # Handles interactions with LLM APIs
├── code_processor.py          # Handles reading, writing, and analyzing code
├── metrics_recorder.py        # Records metrics to Excel file
├── batch_processor.py         # Handles batch processing of multiple files
├── visualization.py           # Visualizes results with charts and reports
├── utils.py                   # Utility functions
├── config.py                  # Configuration settings
├── __init__.py                # Package initialization
├── requirements.txt           # Project dependencies
├── setup.py                   # Package setup script
├── .env.example               # Example environment variables file
└── sample/                    # Sample code for testing
    └── bloated_code.py        # Example of bloated code
```

## Sample Data

The repository includes a sample bloated code file (`sample/bloated_code.py`) that you can use to test the tool:

```bash
python main.py --code_file sample/bloated_code.py --llm_model claude-3-7-sonnet
```

## Metrics Recorded

The tool records the following metrics to an Excel file:

- File name
- LLM model used
- Lines of code before and after optimization
- Percentage reduction in lines of code

## Visualizing Results

After processing one or more files, you can visualize the results:

```bash
python visualization.py --excel bloat_removal_results.xlsx --output_dir reports
```

This will generate charts showing lines of code reduction by LLM model and create a summary report.

## API Keys

To use this tool, you'll need API keys for the LLMs you want to use:

- **Claude**: Get an API key from [Anthropic](https://console.anthropic.com/)
- **GPT-4o**: Get an API key from [OpenAI](https://platform.openai.com/account/api-keys)
- **Gemini**: Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **DeepSeek**: Get an API key from [DeepSeek](https://platform.deepseek.com/)

## Contributing

Contributions to improve the project are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Best Practices

- Always maintain a backup of your original code before running the tool.
- Review the optimized code manually to ensure no critical functionality has been removed.
- If the optimized code has issues, you can restore the original code from the `.bak` file.
- Use the `--export_path` or `--export_dir` options to preserve original files.

## Limitations

- The tool currently supports Python files only.
- LLMs might occasionally remove necessary code, so review the results carefully.
- API rate limits may affect batch processing of many files.
- The size of the code is limited by the context window of the LLM being used.
- Manual review is essential as LLMs may not understand all the specific requirements of your codebase.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project is part of a research study at UC Davis on software bloat detection and removal.
- Thanks to Anthropic, OpenAI, Google, and DeepSeek for providing the LLM services used in this project.