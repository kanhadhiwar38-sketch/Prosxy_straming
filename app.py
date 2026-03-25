import aiohttp
from aiohttp import web
import json
import os

routes = web.RouteTableDef()

BOT_TOKEN = "8413113920:AAGQhaK_6lIjjnjIinQw5f30azHmUSHgdpw"
DB_FILE = "videos.json"

# 📦 Load DB
def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

# 🏠 Home
@routes.get("/")
async def home(request):
    return web.Response(text="Streaming Server Running 🚀")

# 🎬 Stream Route
@routes.get("/stream/{id}")
async def stream_handler(request):
    video_id = request.match_info["id"]
    db = load_db()

    if video_id not in db:
        return web.Response(text="Video not found", status=404)

    file_id = db[video_id]

    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()

        if not data.get("ok"):
            return web.Response(text="Telegram API error", status=500)

        file_path = data["result"]["file_path"]

        video_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        # 🚀 Redirect (FAST STREAMING)
        raise web.HTTPFound(video_url)

    except Exception as e:
        return web.Response(text=f"Error: {str(e)}", status=500)

# 🚀 Run
app = web.Application()
app.add_routes(routes)

if __name__ == "__main__":
    web.run_app(app, port=int(os.environ.get("PORT", 8080)))
