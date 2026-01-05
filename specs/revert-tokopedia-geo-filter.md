# Plan: Revert Tokopedia Search to All Geo Locations

## Task Description
Revert the Tokopedia search functionality to search across all geographic locations instead of being restricted to Bali-based sellers only. This undoes the changes from commit `844dad8` which added the `fcity` parameter with Bali district IDs.

## Objective
Remove the Bali location filter from Tokopedia search URLs so that search results include sellers from all regions of Indonesia, not just Bali.

## Relevant Files
Use these files to complete the task:

- **src/config.py** - Contains the `TOKOPEDIA_BASE_URL` constant that currently includes the Bali `fcity` filter parameter. This is the only file that needs modification.

## Step by Step Tasks

### 1. Remove Bali Location Filter from Config
- Remove the `BALI_CITY_IDS` constant (line 17)
- Update `TOKOPEDIA_BASE_URL` to remove the `fcity` parameter, reverting it to the original format: `https://www.tokopedia.com/search?q=`
- Update the comment from "with Bali location filter" to just "Tokopedia base URL"

### 2. Validate Changes
- Verify the config module compiles correctly
- Confirm the URL format is correct without any geo restrictions

## Acceptance Criteria
- `BALI_CITY_IDS` constant is removed from `src/config.py`
- `TOKOPEDIA_BASE_URL` equals `"https://www.tokopedia.com/search?q="` (no `fcity` parameter)
- The application can import and use the config module without errors

## Validation Commands
Execute these commands to validate the task is complete:

- `uv run python -c "from src.config import TOKOPEDIA_BASE_URL; print(TOKOPEDIA_BASE_URL); assert 'fcity' not in TOKOPEDIA_BASE_URL"` - Verify URL has no geo filter
- `uv run python -c "from src import config; hasattr(config, 'BALI_CITY_IDS') and exit(1)"` - Verify BALI_CITY_IDS constant is removed

## Notes
This is a simple revert task. The original implementation before commit `844dad8` had no geographic restrictions on Tokopedia searches.
