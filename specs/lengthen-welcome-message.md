# Plan: Lengthen Initial Welcome Message

## Task Description
Make the initial welcome message that users see when they start the bot a little longer to provide more context and guidance.

## Objective
Expand the `/start` command welcome message to give users more information about how to use the bot while maintaining its Ukrainian language and friendly tone.

## Relevant Files
Use these files to complete the task:

- `src/response_formatter.py` - Contains the `format_start_message()` function at line 78-85 that returns the welcome message

## Step by Step Tasks

### 1. Update Welcome Message
- Open `src/response_formatter.py`
- Locate the `format_start_message()` function (line 78-85)
- Current message: `"Допомагаю знайти луки на Tokopedia. Кидай фото - кину посилання!"`
- Replace with longer version that includes:
  - A greeting
  - What the bot does
  - How to use it (send a photo)
  - What the user will get back (links to Tokopedia)

Suggested new message:
```
"Привіт! 👋 Я бот, який допомагає знаходити луки на Tokopedia.

Як користуватися:
📸 Надішли мені фото з одягом
🔗 Отримай посилання на схожі речі з Tokopedia

Давай спробуємо - кидай фото!"
```

### 2. Validate the Change
- Ensure the message is still in Ukrainian
- Ensure the message provides clear instructions
- Ensure the message maintains a friendly, casual tone

## Acceptance Criteria
- Welcome message is longer and more informative
- Message is in Ukrainian
- Message explains:
  - What the bot does
  - How to use it (send photo)
  - What the user gets (Tokopedia links)
- Maintains friendly conversational tone

## Validation Commands
Execute these commands to validate the task is complete:

- `uv run python -m py_compile src/response_formatter.py` - Verify syntax is correct

## Notes
The new message should be welcoming but not too long. Consider using emojis to make it visually appealing and easier to scan. The message should guide first-time users on exactly what to do.
