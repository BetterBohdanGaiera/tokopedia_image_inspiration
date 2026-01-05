# Plan: Shorten Initial Welcome Message

## Task Description
Make the initial welcome message that users see when they start the bot shorter and more concise.

## Objective
Reduce the length of the `/start` command welcome message while maintaining its core functionality and Ukrainian language.

## Relevant Files
Use these files to complete the task:

- `src/response_formatter.py` - Contains the `format_start_message()` function at line 78-85 that returns the welcome message

## Step by Step Tasks

### 1. Update Welcome Message
- Open `src/response_formatter.py`
- Locate the `format_start_message()` function (line 78-85)
- Current message: `"Допомагаю знайти луки на Tokopedia. Кидай фото - кину посилання!"`
- Replace with shorter version: `"Кидай фото - знайду луки на Tokopedia!"`

### 2. Validate the Change
- Ensure the message is still in Ukrainian
- Ensure the message still conveys the bot's purpose (send photo → get Tokopedia links)

## Acceptance Criteria
- Welcome message is approximately 50 characters (reduced from 70)
- Message is still in Ukrainian
- Message still explains the core functionality (photo → links)

## Validation Commands
Execute these commands to validate the task is complete:

- `uv run python -m py_compile src/response_formatter.py` - Verify syntax is correct
- `wc -c <<< "Кидай фото - знайду луки на Tokopedia!"` - Confirm new message is ~50 chars

## Notes
The new message `"Кидай фото - знайду луки на Tokopedia!"` (~50 chars) is reduced from the original `"Допомагаю знайти луки на Tokopedia. Кидай фото - кину посилання!"` (70 chars) while maintaining the core call-to-action.
