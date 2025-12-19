"""Main Telegram bot for Tokopedia fashion search."""

import asyncio
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from .config import TELEGRAM_BOT_API, validate_config
from .gemini_analyzer import analyze_image
from .response_formatter import (
    format_analysis_response,
    format_error_message,
    format_start_message,
)

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    if update.message:
        await update.message.reply_text(format_start_message())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    help_text = (
        "Як користуватися ботом:\n\n"
        "1. Надішли фото людини в одязі\n"
        "2. Зачекай кілька секунд\n"
        "3. Отримай посилання на Tokopedia для кожного предмета одягу!\n\n"
        "Команди:\n"
        "/start - Почати роботу з ботом\n"
        "/help - Показати цю довідку"
    )
    if update.message:
        await update.message.reply_text(help_text)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle photo messages."""
    if not update.message or not update.message.photo:
        return

    logger.info(f"Received photo from user {update.effective_user.id if update.effective_user else 'unknown'}")

    # Send "processing" message
    processing_message = await update.message.reply_text(
        "Аналізую фото... Зачекай трохи!"
    )

    try:
        # Get the largest photo (best quality)
        photo = update.message.photo[-1]

        # Download the photo
        file = await context.bot.get_file(photo.file_id)
        photo_bytes = await file.download_as_bytearray()

        logger.info(f"Downloaded photo, size: {len(photo_bytes)} bytes")

        # Analyze the image with Gemini (run in thread to not block other users)
        analysis_result = await asyncio.to_thread(analyze_image, bytes(photo_bytes))

        # Format the response
        response = format_analysis_response(analysis_result)

        # Delete the processing message
        await processing_message.delete()

        # Send the formatted response with original photo
        await update.message.reply_photo(
            photo=bytes(photo_bytes),
            caption=response
        )
        logger.info("Successfully sent analysis response with photo")

    except Exception as e:
        logger.error(f"Error processing photo: {e}", exc_info=True)
        # Delete the processing message
        try:
            await processing_message.delete()
        except Exception:
            pass
        # Send error message
        await update.message.reply_text(format_error_message(str(e)))


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors in the bot."""
    logger.error(f"Exception while handling an update: {context.error}", exc_info=context.error)

    if isinstance(update, Update) and update.message:
        await update.message.reply_text(
            format_error_message("Виникла технічна помилка. Спробуй ще раз!")
        )


def main() -> None:
    """Start the bot."""
    # Validate configuration
    validate_config()

    logger.info("Starting Tokopedia Fashion Bot...")

    # Create the Application
    application = Application.builder().token(TELEGRAM_BOT_API).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Add error handler
    application.add_error_handler(error_handler)

    logger.info("Bot is ready! Starting polling...")

    # Run the bot until interrupted
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
