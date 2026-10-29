# CodeMind AI — Intelligent Code Review and Quality Analysis

## About the Project

CodeMind AI is a Python-based code analysis application built with Streamlit. It helps developers inspect Python code, identify selected code-quality issues, and understand code complexity and maintainability.

## Features

* **Python Syntax Validation:** Checks whether submitted Python code has valid syntax.
* **Static Code Analysis:** Uses Ruff to identify selected code-quality issues.
* **Cyclomatic Complexity:** Uses Radon to measure code complexity.
* **Maintainability Index:** Provides an estimate of code maintainability.
* **Recommendations:** Displays suggestions for improving code quality.
* **Interactive Interface:** Provides a simple web interface using Streamlit.

## Technologies Used

* Python
* Streamlit
* Ruff
* Radon
* Abstract Syntax Trees (AST)

## Project Structure

```text
CodeMind-AI/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .venv/
```

The `.venv` directory is used for local development and should not be uploaded to GitHub.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual repository URL.

### 2. Open the project directory

```bash
cd CodeMind-AI
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment on Windows

For Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the application

```bash
python -m streamlit run app.py
```

Open the local address displayed in the terminal, usually `http://localhost:8501`.

## Limitations

This version performs static code analysis and code-quality measurement. It does not execute submitted code or use a trained machine-learning model to predict bugs.

## Future Enhancements

* Integrate a machine-learning model for defect prediction.
* Add automated unit-test recommendations.
* Support additional programming languages.
* Improve code-quality reports and visualizations.

## Project Status

Initial working prototype.

## Author

Sagala Venkata Krishna
