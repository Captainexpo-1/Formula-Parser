# Formula-Parser

## Overview 
This repo implements AST generation for Airtable formulas. 

## Features
- Tokenizes input formulas into meaningful tokens.
- Parses tokens into an Abstract Syntax Tree (AST).
- Adds a layer of simplification to binary operations to optimize code.

## How to run
1. Clone the repo
2. Run `pip install -r requirements.txt`
3. Run `python3 src/main.py` to open the REPL or use `python3 src/main.py -f <path-to-file>` to run the parser on a file.
