#!/usr/bin/env python3
"""
Telegram bot: send a photo → get model-swapped image back via Fal.ai
Supports nano-banana-2 (default) and Seedream v4.5.

Usage:
  - Send a photo → uses nano-banana-2 by default
  - Send a photo with caption "use seedream" → uses Seedream v4.5
  - Send a photo with caption "use nano banana" → uses nano-banana-2
"""

import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
AI_MODEL_URL_FILE = os.path.join(SKILL_DIR, "ai-model-url.txt")

FAL_API_KEY = os.environ.get("FAL_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

PROMPT = "replicate the exact image as in figure 1, but switch out the model in figure 1 with the model in figure 2"

MODELS = {
    "nano-banana": {
        "url": "https://fal.run/fal-ai/nano-banana-2/edit",
        "params": {
            "num_images": 1,
            "resolution": "1K",
            "aspect_ratio": "4:5",
            "output_format": "png",
        },
        "label": "Nano Banana 2",
    },
    "seedream": {
        "url": "https://fal.run/fal-ai/bytedance/seedream/v4.5/edit",
        "params": {
            "num_images": 1,
            "image_size": "auto_4K",
        },
        "label": "Seedream v4.5",
    },
}


def load_ai_model_url():
    with open(AI_MODEL_URL_FILE) as f:
        return f.read().strip()


def detect_model(caption: str) -> str:
    """Return model key based on caption text. Defaults to nano-banana."""
    if caption:
        caption_lower = caption.lower()
        if "seedream" in caption_lower:
            return "seedream"
        if "nano" in caption_lower or "banana" in caption_lower:
            return "nano-banana"
    return "nano-banana"


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = update.message.caption or ""
    model_key = detect_model(caption)
    model = MODELS[model_key]

    await update.message.reply_text(f"Got it! Using {model['label']}, hang tight...")

    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    scene_url = file.file_path

    ai_model_url = load_ai_model_url()

    payload = {
        "prompt": PROMPT,
        "image_urls": [scene_url, ai_model_url],
        **model["params"],
    }

    response = requests.post(
        model["url"],
        headers={
            "Authorization": f"Key {FAL_API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
    )

    if not response.ok:
        await update.message.reply_text(f"Fal.ai error: {response.status_code}\n{response.text}")
        return

    result_url = response.json()["images"][0]["url"]
    await update.message.reply_photo(photo=result_url, caption=f"Done! Generated with {model['label']}")


async def handle_non_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send me a photo to swap the model.\n\n"
        "Add a caption to choose the model:\n"
        "• No caption → Nano Banana 2 (default)\n"
        "• \"use seedream\" → Seedream v4.5\n"
        "• \"use nano banana\" → Nano Banana 2"
    )


def main():
    if not FAL_API_KEY:
        print("ERROR: FAL_API_KEY environment variable not set.")
        return
    if not TELEGRAM_BOT_TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN environment variable not set.")
        return

    print("Bot is running... Send a photo to your bot in Telegram.")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(~filters.PHOTO, handle_non_photo))
    app.run_polling()


if __name__ == "__main__":
    main()
