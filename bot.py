import os
import json
from pyrogram import Client, filters

# 🔑 Telegram Credentials
API_ID = 37454234  # 🔴 my.telegram.org से लो
API_HASH = "9d14b26020c10dab5e3e82c211328ae0"
BOT_TOKEN = "8413113920:AAGQhaK_6lIjjnjIinQw5f30azHmUSHgdpw"

# 🌐 Replace with your Render URL
BASE_URL = "https://prosxy-straming.onrender.com"

DB_FILE = "videos.json"

app = Client(
    "video_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# 📦 Load DB
def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

# 💾 Save DB
def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# 🚀 Start Command
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("✅ Bot is running perfectly!")

# 🎬 VIDEO HANDLER (UPDATED FIXED)
@app.on_message(filters.video | filters.document | filters.forwarded)
async def video_handler(client, message):
    print("📥 New message received")

    db = load_db()

    try:
        # 🎬 file_id extract
        if message.video:
            file_id = message.video.file_id
            print("🎥 Video detected")
        elif message.document:
            file_id = message.document.file_id
            print("📁 Document detected")
        else:
            print("❌ Not a video/document")
            return

        # 🆔 Generate new ID
        new_id = str(len(db) + 1)

        # 💾 Save
        db[new_id] = file_id
        save_db(db)

        # 🔗 Generate link
        link = f"{BASE_URL}/stream/{new_id}"

        # 📤 Reply
        await message.reply_text(
            f"✅ Video Added Successfully!\n\n"
            f"🎬 ID: {new_id}\n"
            f"🔗 Link: {link}"
        )

        print(f"✅ Saved ID {new_id}")

    except Exception as e:
        print("❌ Error:", e)
        await message.reply_text("⚠️ Error occurred")

# 🚀 Run bot
print("🔥 BOT STARTING...")
app.run()
