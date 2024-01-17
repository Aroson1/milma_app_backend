# Milama Food Ordering App Backend
This is the backend part for the Milma food ordering app.

<!-- [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)-->

## Installation

To install and set up the project:

1. Clone the repository.
2. Navigate to the project directory.
3. Make a new virtual environment.
    ```bash
    python3 -m venv .
    ```
4. Install the dependencies using the following command:
    ```bash
    pip install -r requirements.txt
    ```
5. Add the .env file to the root directory.

## Usage

```bash
uvicorn --port 1234 main:app --reload
```
_Note: Make sure that the port is set to 1234._
