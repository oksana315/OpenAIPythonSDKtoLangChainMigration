# Python Project

This is a Python project template with a basic structure.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the main script:
```bash
python src/main.py
```

## Development

This project includes several development tools:
- `pytest` for testing
- `black` for code formatting
- `flake8` for code linting

To format your code:
```bash
black .
```

To run linting:
```bash
flake8
```

To run tests (once implemented):
```bash
pytest
```

## Project Structure

```
.
├── README.md
├── requirements.txt
└── src/
    └── main.py
``` 