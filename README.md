# PyEmail Assistant

**Version:** 0.1

**OS:** Linux

**Author:** Brent Bradford

## Description

SongDatabase is a class project that uses an sqlite3 database to manage songs.

## Requirements

### Poetry

- [Poetry 1.8.2+](https://python-poetry.org/)

### Python

- [Python 3.10 - 3.13](https://www.python.org/downloads/)

#### Packages

1. pyyaml
2. pyqt6

## Installation - Linux

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to your Path
export Path="$HOME/.local/bin:$PATH"

# Verify Poetry Installation
poetry --version

# Install PyQT6 Dependencies (Ubuntu Example)
sudo apt install libgl1 libxkbcommon-x11-0 libegl1-mesa libxcb-xinerama0 libxcb-cursor0 libx11-xcb1 libglu1-mesa qtwayland5

# Clone the repository and change your directory
git clone https://github.com/bcbradford/SongDatabase.git
cd SongDatabase

# Install PyEmailAssistant
poetry install
```
## Usage

```bash
poetry run songdatabase
```

## Alternative Run: Running app.py

```bash
# Start Poetry Shell
poetry shell

# Change Directory to App.py Directory
cd src/songdatabase/

# Run App
python3 app.py
```

## License

### SongDatabase
Copyright (c) 2024 Brent Bradford

This product is licensed under the Apache License 2.0 (see LICENSE.md for details).
