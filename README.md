# Mandi Price Backend

## Overview
This repository contains the backend code for a mandi (market) price lookup system designed to help users query and analyze crop pricing from various locations.

## Features
- FastAPI-powered backend in Python
- SQLite database for storing and querying mandi prices
- CSV & JSON data import
- Modular code for CRUD operations and utility functions
- No frontend files tracked (`indexx.html` excluded; backend-only)

## Quick Start
1. Clone this repo and navigate to the root directory.
2. Create a virtual environment:
python -m venv venv

text
3. Activate the environment and install dependencies:
pip install -r requirements.txt

text
4. Run the backend:
python app/main.py

text

## Structure

| Folder/File         | Description                              |
|---------------------|------------------------------------------|
| `app/`              | Backend source code (FastAPI, models)    |
| `data/`             | Database, CSVs, and support files        |
| `requirements.txt`  | Python dependencies                      |
| `.gitignore`        | Specifies files/folders Git should ignore|

## Usage
Send requests to your API endpoints as defined in `main.py`. See `README.md` or in-code docstrings for example queries.

## License
MIT License
Steps to Deploy Backend on GitHub
Initialize Git (if not already):

text
git init
Add .gitignore and README.md to the project root.

Stage & commit:

text
git add .
git commit -m "Initial backend commit with .gitignore and README"
Create a GitHub repository (from github.com).

Link your local repo to it:

text
git remote add origin https://github.com/<your-username>/<repo-name>.git
Push your code:

text
git push origin master