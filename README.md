# AI AGENT
A Python CLI that allows a Google Gemini model to interact with the file system using natural language commands.

## Overview
This tool provides a command-line interface where Google Gemini-powered agent can:
- Explore and query files and directories
- Read file contents
- Execute Python scripts
- Write and modify files
- Respond with context-aware explanations

## Getting Started
### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) installed
- A [Google Gemini API](https://ai.google.dev/gemini-api/docs) key
- git

### Setup
clone the repository and install dependencies using [uv](https://github.com/astral-sh/uv):
```
git clone https://github.com/rgibby818/ai-agent.git
cd ai-agent
uv sync
```
create a `.env` file at the root of the directory and enter in your Google Gemini API key, Model, and your working directory:
```
GEMINI_API_KEY='<API_KEY_HERE>'
MODEL='gemini-2.5-flash'
```
To change the working directory change the `WORKING_DIR` variable in the `configs.py` file.

### Usage
Run the cli with:
```
uv run python main.py "Your prompt here"
```
Example:
```
uv run python main.py "There is a bug in my code. It outputs 20 but it should be 17."
```
```
uv run python main.py "show the contents of main.py" --verbose
```

## Notes and Warnings
### This agent has access to your local file system.
Be cautious when running prompts that could modify or delete files, especially when point `WORKING_DIR` at sensitive directories.