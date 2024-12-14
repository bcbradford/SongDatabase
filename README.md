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

## Instructions

### Create Entities

To create the entities for the database:

1. Select the Database Menu
2. Select Create Entry
3. Select the entity type form the table combo box
4. Press the submit button.
5. A dialog window will be displayed asking for user input.
6. Input the value for the entity and press submit.

The entity will be created

### Delete Entities

To delete the entities in the database:

1. Select the Database Menu
2. Select Delete Entry
3. Select the entity type in the table combo box.

The delete combo box will be automatically populated will entities
that can be deleted.

4. Select the entity to delete in the delete combo box.
5. Press Submit

You will be prompted if you want to delete the entity.
If you press yes, the entity will be deleted.

### Update Entities

To update the entities in the database:

1. Select the Database Menu
2. Select Update Entry
3. Select the entity type in the table combo box.

This will automatically populate the update combo box with database entities.

4. Select the entity to update in the table combo box.
5. Press submit

You will be prompted to input the updated field in a new dialog window.
Pressing submit with a new title to update the entity, or the x in the window
to cancel.

### Update Songs

To update the songs in the database, ensure you have
the song already created in the database. Then:

1. Select the Database Menu
2. Select the song from the combo box and press submit

You will be prompted to select the Artist, Category, and Album
to assign to the song. These fields are automatically populated
with the existing entities in the database.

3. Select the value of each entity from their combo boxes.
4. Press submit.

The song will be updated with its respective artist, category, and
album.

## License

### SongDatabase
Copyright (c) 2024 Brent Bradford

This product is licensed under the Apache License 2.0 (see LICENSE.md for details).
