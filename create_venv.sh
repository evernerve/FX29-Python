#!/bin/bash

set -e

echo_msg() {
    echo -e "\033[1;32m$1\033[0m"
}

VENV_DIR=".sensor"         
REQUIREMENTS_FILE="requirements.txt"

if [ ! -d "$VENV_DIR" ]; then
    echo_msg "Creating virtual environment in '$VENV_DIR'..."
    python3 -m venv "$VENV_DIR"
else
    echo_msg "Virtual environment '$VENV_DIR' already exists."
fi

source "$VENV_DIR/bin/activate"

if [ -f "$REQUIREMENTS_FILE" ]; then
    echo_msg "Installing packages from '$REQUIREMENTS_FILE'..."
    pip install --upgrade pip
    pip install -r "$REQUIREMENTS_FILE"
else
    echo_msg "'$REQUIREMENTS_FILE' not found. Skipping package installation."
fi


echo_msg "Virtual environment setup complete."


