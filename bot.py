from pyrogram import Client, filters
import json
import os

API_ID = 37454234        # 🔴 my.telegram.org से लो
API_HASH = "9d14b26020c10dab5e3e82c211328ae0"
BOT_TOKEN = "8413113920:AAGQhaK_6lIjjnjIinQw5f30azHmUSHgdpw"

app = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

DB_FILE = "videos.json"

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

# 🎬 Video detect (channel/group/forward)
@app.on_message(filters.video)
async def video_handler(client, message):
    db = load_db()

    new_id = str(len(db) + 1)
    file_id = message.video.file_id

    db[new_id] = file_id
    save_db(db)

    link = f"https://prosxy-straming.onrender.com/stream/{new_id}"

    await message.reply_text(
        f"✅ Video Added!\n\n🎬 ID: {new_id}\n🔗 Link: {link}"
    )

app.run()
