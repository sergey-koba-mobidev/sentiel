#!/bin/sh

# Update the code
git pull

# Check config file
python check_config.py

# Run the Sentinel
python sentinel.py

