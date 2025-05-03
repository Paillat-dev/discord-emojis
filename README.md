# Discord Emojis

A Python tool that automatically fetches and extracts the latest emoji data from Discord.

## Overview

This project automatically downloads the latest Discord build from the [Discord-Datamining](https://github.com/Discord-Datamining/Discord-Datamining) repository, extracts emoji data, and saves it in a structured JSON format. It runs as a GitHub Actions workflow twice a week and opens a pull-request to keep the emoji data up-to-date, without manual intervention.

## How It Works

- GitHub Actions workflow runs automatically twice per week
- Downloads the latest Discord build
- Extracts emoji information
- Saves data in a standardized JSON format
- Tracks changes using hash comparison to avoid unnecessary updates
- Detects and reports unhandled UTF-16 surrogate pairs

## Technical Details

The project uses:
- Python 3.13+
- Dependencies:
  - json5
  - requests

## Output

The emoji data is saved in `build/emojis.json` in the following format:

```json
{
    "emojis": [
        {
            "names": [
                "grinning",
                "grinning_face"
            ],
            "surrogates": "😀",
            "unicodeVersion": 6.1,
            "spriteIndex": 0
        },
        // More emoji entries...
    ],
    "emojisByCategory": {
        "people": [
            0,
            509
        ],
        // More categories...
    },
    "nameToEmoji": {
        "100": 1410,
        "1234": 1488,
        "grinning": 0,
        // More name mappings...
    },
    "surrogateToEmoji": {
        "😀": 0,
        "😃": 1,
        "😄": 2,
        // More surrogate mappings...
    },
    "numDiversitySprites": 310,
    "numNonDiversitySprites": 1614
}
```

### Format Explanation

- **emojis**: Array of emoji objects containing:
  - **names**: Array of names/aliases for the emoji
  - **surrogates**: Unicode representation of the emoji
  - **unicodeVersion**: Version where the emoji was introduced
  - **spriteIndex**: Index in Discord's sprite sheet

- **emojisByCategory**: Object mapping category names to arrays of starting and ending indices in the emoji array

- **nameToEmoji**: Mapping of emoji names to their index in the emoji array (used for quick lookups)

- **surrogateToEmoji**: Mapping of emoji unicode characters to their index in the emoji array (used for quick lookups)

- **numDiversitySprites**: Number of skin tone modifier sprites available (e.g., different skin tones for hand gestures)

- **numNonDiversitySprites**: Number of standard emoji sprites that don't have skin tone modifiers

## Easy Access

The easiest way to access the emojis data is via the direct raw GitHub URL:

```
https://raw.githubusercontent.com/Paillat-dev/discord-emojis/refs/heads/master/build/emojis.json
```

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