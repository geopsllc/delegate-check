#!/bin/bash

sudo apt install -y python3-aiohttp

# Create your local config from the template (config.py is git-ignored, so pulls never overwrite it)
[ -f config.py ] || cp config.example.py config.py
