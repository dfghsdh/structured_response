# Structured Response Generator

This project contains a Python script that generates structured responses (JSON, HTML, XML, YAML) based on given data and structure templates using the Ollama API.

## Overview

The `structured_response.py` script is designed to:

1. Take input data and a structure template
2. Use the Ollama API to generate a response that fits the given structure
3. Validate the generated response
4. Retry if the response is invalid (up to 5 attempts)

The script supports four types of structured outputs:
- JSON
- HTML
- XML
- YAML

## Requirements

- Python 3.x
- Ollama API running locally on port 11434
- Required Python packages (installed automatically by the setup script):
  - requests
  - PyYAML
  - beautifulsoup4

## Files

- `structured_response.py`: Main Python script
- `requirements.txt`: List of required Python packages
- `setup_and_run.sh`: Bash script to set up the environment and run the Python script

## Setup and Running

1. Ensure you have Python 3.x installed on your system.
2. Make sure the Ollama API is running locally on port 11434.
3. Run the setup script:

   ```
   chmod +x setup_and_run.sh
   ./setup_and_run.sh
   ```

   This script will:
   - Create a virtual environment
   - Install required packages
   - Run the Python script

## How It Works

1. The script defines test cases for each supported structure type (JSON, HTML, XML, YAML).
2. For each test case, it calls the `process_structured_output` function.
3. This function sends a prompt to the Ollama API, requesting a structured response.
4. The response is extracted and validated.
5. If invalid, the script retries up to 5 times with refined prompts.
6. Results and attempt logs are printed for each test case.

## Customization

You can modify the `test_cases` in the `main()` function of `structured_response.py` to test different data and structures.

## Troubleshooting

If you encounter any issues:
1. Ensure Ollama API is running and accessible.
2. Check that all required packages are installed correctly.
3. Verify that your Python version is compatible (3.x).
4. Review the console output for any error messages.

## Contributing

Feel free to fork this repository and submit pull requests for any improvements or bug fixes.

## License

[Specify your license here, e.g., MIT License]
