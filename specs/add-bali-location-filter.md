# Plan: Add Bali Location Filter to Tokopedia URLs

## Task Description
Modify the Tokopedia URL generation to always include a Bali location filter (`fcity` parameter) in all search URLs. This will restrict search results to sellers located in Bali, Indonesia.

## Objective
All generated Tokopedia search URLs will include the Bali city filter parameter, changing the format from:
- `https://www.tokopedia.com/search?q=<query>`

To:
- `https://www.tokopedia.com/search?fcity=258,259,260,261,262,263,264,265,476,266&q=<query>`

## Problem Statement
Currently, the bot generates Tokopedia search URLs that show results from all sellers across Indonesia. The user wants to filter results to only show sellers from Bali to ensure:
- Faster local shipping
- Support for local Bali sellers
- More relevant results for users in the Bali area

## Solution Approach
Add the Bali city IDs as a configuration constant and modify the URL generation function to always include the `fcity` parameter before the search query.

The Bali city filter includes these city/district IDs:
- 258, 259, 260, 261, 262, 263, 264, 265, 476, 266

## Relevant Files
Use these files to complete the task:

- **`src/config.py`** - Add Bali city IDs constant and modify base URL configuration
- **`src/tokopedia_search.py`** - Update `generate_tokopedia_url()` function to include fcity parameter

## Step by Step Tasks
IMPORTANT: Execute every step in order, top to bottom.

### 1. Add Bali City Filter Configuration
- Add `BALI_CITY_IDS` constant to `src/config.py` with value `"258,259,260,261,262,263,264,265,476,266"`
- Update `TOKOPEDIA_BASE_URL` to include the fcity parameter:
  ```python
  BALI_CITY_IDS = "258,259,260,261,262,263,264,265,476,266"
  TOKOPEDIA_BASE_URL = f"https://www.tokopedia.com/search?fcity={BALI_CITY_IDS}&q="
  ```

### 2. Verify URL Generation Function
- Confirm `src/tokopedia_search.py` `generate_tokopedia_url()` function works correctly with the updated base URL
- No changes needed to this file since it already uses `TOKOPEDIA_BASE_URL`

### 3. Test the Changes
- Run a quick test to verify URLs are generated correctly with the Bali filter
- Example input: `"Bando tanduk iblis merah murah"`
- Expected output: `https://www.tokopedia.com/search?fcity=258,259,260,261,262,263,264,265,476,266&q=Bando%20tanduk%20iblis%20merah%20murah`

## Acceptance Criteria
- All generated Tokopedia URLs include the `fcity=258,259,260,261,262,263,264,265,476,266` parameter
- The fcity parameter appears before the `q` parameter in the URL
- Search queries are still properly URL-encoded
- The bot continues to function normally with no breaking changes

## Validation Commands
Execute these commands to validate the task is complete:

- `uv run python -c "from src.config import TOKOPEDIA_BASE_URL; print(TOKOPEDIA_BASE_URL)"` - Verify base URL includes fcity parameter
- `uv run python -c "from src.tokopedia_search import generate_tokopedia_url; print(generate_tokopedia_url('Bando tanduk iblis merah murah'))"` - Verify complete URL generation
- `uv run python -m py_compile src/config.py src/tokopedia_search.py` - Ensure code compiles without errors

## Notes
- The Bali city IDs (`258,259,260,261,262,263,264,265,476,266`) represent various districts within Bali province on Tokopedia's location system
- This is a minimal change that only affects the configuration constant - no logic changes required
- If location filtering needs to be made configurable in the future, the `BALI_CITY_IDS` constant can be moved to environment variables
