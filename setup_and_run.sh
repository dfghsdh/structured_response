#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Print commands and their arguments as they are executed
set -x

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip to the latest version
pip install --upgrade pip

# Install wheel package
pip install wheel

# Install dependencies with verbose output
pip install -v -r requirements.txt

# If the above command fails, try installing packages one by one
if [ $? -ne 0 ]; then
    echo "Failed to install all packages at once. Trying one by one..."
    while read requirement; do
        pip install -v $requirement || echo "Failed to install $requirement"
    done < requirements.txt
fi

# Print installed packages for debugging
pip list

# Run the Python script
if [ "$1" == "--verbose" ]; then
    python structured_response.py --verbose
else
    python structured_response.py
fi

# Deactivate the virtual environment
deactivate
