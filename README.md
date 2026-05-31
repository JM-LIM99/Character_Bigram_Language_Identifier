# Character Bigram Language Identifier


A lightweight language identification system based on character bigram frequency analysis.

## Approach

Extracts the top 10 most frequent character bigram from input text and compares them against pre-built per-language reference models using intersection scroing.

## Results.
Test Files: 1,232.

Correct : 1,090

Accuracy : 88.5%

## Project Structure

Character-Bigram-Language-ID/
├── README.md
├── evaluation_models.py  # Runs evaluation on test set
├── generate_reference.py # Builds per-language bigram reference models    
└── utils/
    ├── text_analyzer.py     # Bigram extraction and analysis
    └── language_evaluator.py # Scoring and metrics

# Stack
Python, pathlib, json
