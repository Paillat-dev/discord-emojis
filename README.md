# Discord Emojis

A Python tool that automatically fetches and extracts the latest emoji data from Discord.

## Overview

This project automatically downloads the latest Discord build from the [Discord-Datamining](https://github.com/Discord-Datamining/Discord-Datamining) repository, extracts emoji data, and saves it in a structured JSON format. It runs as a GitHub Actions workflow twice a week to keep the emoji data up-to-date without manual intervention.

## How It Works

- GitHub Actions workflow runs automatically twice per week
- Downloads the latest Discord build
- Extracts emoji information
- Saves data in a standardized JSON format
- Tracks changes using hash comparison to avoid unnecessary updates
- Detects and reports UTF-16 surrogate pairs

## Technical Details

The project uses:
- Python 3.13+
- Dependencies:
  - json5
  - orjson
  - requests

## Output

The emoji data is saved in `build/emojis.json` in the following format:
```json
{
    "emojis": [
        {
            "name": "emoji_name",
            "id": "emoji_id",
            ...
        },
        ...
    ]
}
```

The main emojis.json file in the root directory is the updated version that consumers can access via GitHub raw URLs or by cloning this repository.

## Development

For local development or testing:

```bash
# Install dependencies using uv
uv sync --dev

# Run the update script manually
uv run src
```

Note: Local execution should only be done during development. In production, the script runs automatically through GitHub Actions.

The script will:
1. Download the latest Discord build
2. Extract emoji information
3. Save the data to `build/emojis.json`
4. Generate a hash file to track changes

If no changes are detected compared to the previous run, the script will exit with status code 3.