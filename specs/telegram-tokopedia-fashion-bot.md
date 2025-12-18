# Plan: Telegram Tokopedia Fashion Bot

## Task Description
Build a Telegram bot (@tokopedia_crazy_shopper_bot) that analyzes uploaded images using Google Gemini Pro to identify clothing items worn by people in photos. The bot then generates Tokopedia search URLs for each identified item, prioritizing **CHEAP, TRASHY, CRAZY** options suitable for a "beach trash party" theme (Zatoka vibes, Verka Serduchka style).

**CRITICAL LANGUAGE REQUIREMENTS:**
- **Bot responses**: ALWAYS in UKRAINIAN
- **Tokopedia search queries**: ALWAYS in INDONESIAN (for Tokopedia Indonesia)

The bot should provide creative upsell suggestions and complementary "crazy ideas" alongside the main product recommendations.

## Objective
Create a fully functional Telegram bot that:
1. Listens for image uploads in any chat where it's added
2. Uses Gemini Pro vision capabilities to analyze clothing in images
3. Generates accurate Tokopedia search URLs based on identified items
4. Returns formatted responses with product links and upsell suggestions

## Problem Statement
Users want to quickly find cheap, fun clothing items on Tokopedia that match outfits they see in photos. This is specifically for "beach trash party" events where participants need affordable, one-time-use costume pieces. Manual searching is time-consuming and requires knowing the right Indonesian search terms.

## Solution Approach
Build a Python-based Telegram bot using:
- `python-telegram-bot` library for Telegram API integration
- `google-generativeai` SDK for Gemini Pro vision analysis
- Structured prompts that guide Gemini to identify clothing with Indonesian Tokopedia search terms
- Pre-loaded reference data from `beach-party-tokopedia-looks.json` to enhance search accuracy

## Relevant Files

### Existing Files
- `/Users/bohdanpytaichuk/Documents/TokopediaImageInspiration/beach-party-tokopedia-looks.json` - Reference data with 80+ Tokopedia search examples covering beach/trashy party looks, used as context for Gemini prompts
- `/Users/bohdanpytaichuk/Documents/TokopediaImageInspiration/.env` - Environment variables (GEMINI_API_KEY exists, need to add TELEGRAM_BOT_API)

### New Files
- `src/bot.py` - Main Telegram bot entry point with handlers
- `src/gemini_analyzer.py` - Gemini Pro image analysis module
- `src/tokopedia_search.py` - Tokopedia URL generation utilities
- `src/response_formatter.py` - Format bot responses with links and suggestions
- `src/config.py` - Configuration and environment variable loading
- `pyproject.toml` - Project dependencies (uv-managed)

## Implementation Phases

### Phase 1: Foundation
- Set up project structure with uv
- Configure environment variables
- Create base bot skeleton with image handling

### Phase 2: Core Implementation
- Implement Gemini Pro vision integration with structured prompts
- Build Tokopedia URL generator using reference data patterns
- Create response formatter with the required output format

### Phase 3: Integration & Polish
- Connect all components in the bot handler
- Add error handling and rate limiting
- Test with sample images

## Step by Step Tasks

### 1. Set Up Project Structure
- Create `src/` directory for source code
- Initialize `pyproject.toml` with dependencies:
  - `python-telegram-bot>=21.0`
  - `google-generativeai>=0.3.0`
  - `python-dotenv>=1.0.0`
- Add TELEGRAM_BOT_API to `.env` file

### 2. Create Configuration Module
- Create `src/config.py` to load environment variables
- Load GEMINI_API_KEY and TELEGRAM_BOT_API from .env
- Load reference data from `beach-party-tokopedia-looks.json`
- Create base Tokopedia URL constant: `https://www.tokopedia.com/search?q=`

### 3. Implement Gemini Analyzer
- Create `src/gemini_analyzer.py`
- Initialize Gemini model using latest available (December 2025):
  - **`gemini-2.5-pro`** - Best accuracy for fashion analysis (recommended)
  - **`gemini-2.5-flash`** - Best price-performance balance
  - **`gemini-3-pro-preview`** - Newest model (preview, most advanced multimodal)
- Build structured prompt that:
  - Asks Gemini to identify each clothing item on each person
  - Requests Indonesian search terms for Tokopedia
  - Includes reference examples from the JSON data
  - Asks for "crazy complementary ideas"
- Return structured JSON with identified items

### 4. Build Tokopedia URL Generator
- Create `src/tokopedia_search.py`
- Function to URL-encode Indonesian search queries
- Function to generate raw Tokopedia URLs
- Matcher to find similar items in reference JSON for better search terms

### 5. Create Response Formatter
- Create `src/response_formatter.py`
- Format response as:
```
Here are the clothes that this person wears:

**[Person 1]**
- [Item Name]: [Tokopedia URL]
- [Item Name]: [Tokopedia URL]

**You might also like:**
- [Crazy idea 1]: [Tokopedia URL]
- [Crazy idea 2]: [Tokopedia URL]
```
- Handle multiple people in image
- Generate raw URLs (no markdown link formatting)

### 6. Implement Main Bot
- Create `src/bot.py`
- Set up Telegram bot with Application builder
- Add photo message handler that:
  1. Downloads the image from Telegram
  2. Sends image to Gemini for analysis
  3. Generates Tokopedia URLs for each item
  4. Formats and sends response
- Add `/start` command with usage instructions
- Add error handler for graceful failure

### 7. Create Entry Point
- Add `__main__.py` or update `bot.py` to run with `uv run python -m src.bot`
- Implement async main loop with proper shutdown handling

### 8. Test and Validate
- Run the bot locally
- Test with sample fashion images
- Verify Tokopedia URLs are correctly formatted
- Check response format matches requirements

## Testing Strategy

### Unit Tests
- Test URL encoding with Indonesian characters
- Test response formatter output format
- Test Gemini prompt structure

### Integration Tests
- Test bot startup with valid credentials
- Test image download from Telegram
- Test end-to-end with mock Gemini response

### Manual Testing
- Send test images to bot in Telegram
- Verify links work on Tokopedia
- Check multiple people detection

## Acceptance Criteria
- [ ] Bot starts without errors using `uv run python -m src.bot`
- [ ] Bot responds to image uploads in group chats and DMs
- [ ] Each response includes at least 2-3 clothing items with Tokopedia URLs
- [ ] URLs are raw format (https://www.tokopedia.com/search?q=...)
- [ ] Response includes "You might also like" section with creative suggestions
- [ ] URLs use proper Indonesian search terms
- [ ] Bot handles errors gracefully (invalid images, API failures)

## Validation Commands

Execute these commands to validate the task is complete:

- `uv run python -m py_compile src/bot.py src/gemini_analyzer.py src/tokopedia_search.py` - Verify code compiles
- `uv run python -m src.bot` - Start the bot (requires valid API keys)
- Send a test image to @tokopedia_crazy_shopper_bot in Telegram

## Notes

### Dependencies to install
```bash
uv add python-telegram-bot google-generativeai python-dotenv
```

### Environment Variables Required
```env
GEMINI_API_KEY=your_gemini_api_key
TELEGRAM_BOT_API=your_telegram_bot_token
```

### Gemini Model Selection (December 2025)

Available models for vision/multimodal tasks:

| Model | Use Case | Notes |
|-------|----------|-------|
| `gemini-2.5-pro` | **Recommended** - Best accuracy | Stable, excellent for fashion analysis |
| `gemini-2.5-flash` | Cost-efficient | 3x faster, great price-performance |
| `gemini-3-pro-preview` | Cutting-edge | Latest preview, most advanced multimodal |
| `gemini-2.5-flash-lite` | Budget option | Fastest, lowest cost |

For this bot, use **`gemini-2.5-pro`** for best clothing identification accuracy.

### Example Gemini Prompt Structure

```text
Ти - експерт з моди для БОЖЕВІЛЬНОЇ ПЛЯЖНОЇ ВЕЧІРКИ (Beach Trash Party, Zatoka vibes, Verka Serduchka style).

Проаналізуй це зображення та визнач ВСІ предмети одягу на кожній людині.

ВАЖЛИВО:
- Відповідай УКРАЇНСЬКОЮ мовою
- Пошукові запити для Tokopedia - ІНДОНЕЗІЙСЬКОЮ
- Шукай ДЕШЕВІ, ТРЕШОВІ, БОЖЕВІЛЬНІ варіанти (для одноразової вечірки!)
- Пріоритет: дешевизна > якість

Для кожного предмета надай:
1. Назва українською (описово, смішно)
2. Пошуковий запит для Tokopedia (ІНДОНЕЗІЙСЬКОЮ!)
3. Категорія (top, bottom, accessory, footwear, headwear)

Також КРЕАТИВНО запропонуй 2-3 БОЖЕВІЛЬНІ аксесуари, які б доповнили цей образ!
Будь креативним - підбери те, що зробить образ ще БІЛЬШ АБСУРДНИМ та PARTY-READY.
Натхнення (але не копіюй буквально!):
- Zatoka vibes, Verka Serduchka style, Baryga mode, Sanatorium aesthetic, Disco trash

Приклади пошукових запитів:
- Гавайська сорочка → "Kemeja hawaii merah"
- Mankini → "Mankini hijau" або "Borat costume"
- Золотий ланцюг → "Kalung emas rantai besar hip hop"
- Надувний єдиноріг → "Ban renang unicorn dewasa"

Поверни JSON:
{
  "people": [
    {
      "description_ua": "Опис людини українською",
      "items": [
        {"name_ua": "Назва українською", "search_query_id": "Indonesian query", "category": "..."}
      ]
    }
  ],
  "crazy_ideas": [
    {"name_ua": "Назва українською", "search_query_id": "Indonesian query", "vibe": "Zatoka/Serduchka/Baryga"}
  ]
}
```

### Bot Response Format (UKRAINIAN!)

The bot should ALWAYS respond in **UKRAINIAN** with Indonesian search URLs:

```text
Ось що носить ця людина:

Рожева гавайська сорочка
https://www.tokopedia.com/search?q=Kemeja%20hawaii%20pink

Короткі джинсові шорти
https://www.tokopedia.com/search?q=Celana%20jeans%20pendek%20pria

Сонцезахисні окуляри ретро
https://www.tokopedia.com/search?q=Kacamata%20hitam%20vintage

---
Можливо тобі сподобається (CRAZY PARTY VIBES):

Надувний єдиноріг (Zatoka style!)
https://www.tokopedia.com/search?q=Ban%20renang%20unicorn%20dewasa

Окуляри-зірки (Verka Serduchka!)
https://www.tokopedia.com/search?q=Kacamata%20bintang%20besar

Золотий ланцюг hip-hop (Baryga mode!)
https://www.tokopedia.com/search?q=Kalung%20emas%20rantai%20besar%20hip%20hop
```

### Upsell Inspiration (NOT HARDCODED!)

Gemini should **creatively suggest** crazy party accessories based on the outfit in the image. These are just **EXAMPLES FOR INSPIRATION** - the AI should come up with relevant, fun suggestions that complement the specific look:

**Example vibes to inspire (not to copy!):**
- Zatoka vibes: inflatables, beach trash aesthetic
- Verka Serduchka style: crazy glasses, sparkles, over-the-top
- Baryga mode: gold chains, leather, 90s gangster
- Sanatorium vibes: grandma/grandpa vacation aesthetic
- Disco/Party: glitter, feathers, disco balls

**The key principle:** Suggest items that would make the outfit MORE RIDICULOUS and PARTY-READY. Be creative! Match the energy of the original outfit.
