# 🚧 WORK IN PROGRESS

## 🛠 How to Set Up the Project

### 📦 Dependency Management

This project uses [Poetry](https://python-poetry.org/) to manage dependencies and environments.

Useful links:
- [Poetry Basic Usage](https://python-poetry.org/docs/basic-usage/)
- [Poetry CLI Reference](https://python-poetry.org/docs/cli/)

### 🧪 Installation

Run this command **once**, or **whenever you change `pyproject.toml`**:
```bash
poetry install
```

## 🚀 How to Launch a Script

Use the following command to run a script defined in your project:
```bash
poetry run [script_name]
```

Example:
```bash
poetry run test_tle
```

Alternatively, run a specific Python file directly:
```bash
poetry run python src/inorbit/test_tle.py
```

## 🧱 How to Create a New Script

Create your new script, for example:
```bash
touch src/inorbit/my_new_script.py
```

Then add the script to the pyproject.toml :
```bash
my_new_script = "inorbit.my_new_script:main"
```
