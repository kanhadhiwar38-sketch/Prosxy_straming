import aiohttp
from aiohttp import web

routes = web.RouteTableDef()

# 🔑 अपना Telegram Bot Token डालो
BOT_TOKEN = "YOUR_BOT_TOKEN"

# 🎬 Video ID → Telegram file_id mapping
video_db = {
    "315": "AgADQRxxxxxxxxxxxx",  # अपना file_id डालो
}

# 🏠 Home Route (test)
@routes.get("/")
async def home(request):
    return web.Response(text="Bot Running 🚀")

# 🎬 Stream Route (IMPORTANT)
@routes.get("/stream/{id}")
async def stream_handler(request):
    video_id = request.match_info["id"]

    # ❌ Video नहीं मिला
    if video_id not in video_db:
        return web.Response(text="Video not found", status=404)

    file_id = video_db[video_id]

    try:
        # 📡 Telegram से file_path लो
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()

        if not data.get("ok"):
            return web.Response(text="Telegram API error", status=500)

        file_path = data["result"]["file_path"]

        # 🚀 Direct Telegram CDN link
        video_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        # ⚡ Redirect (NO PROXY = FAST)
        raise web.HTTPFound(video_url)

    except Exception as e:
        return web.Response(text=f"Error: {str(e)}", status=500)


# 🔐 Optional Secure Route (token system)
@routes.get("/secure/{id}")
async def secure_stream(request):
    video_id = request.match_info["id"]
    token = request.query.get("token")

    if token != "my_secure_token_123":
        return web.Response(text="Invalid token", status=403)

    if video_id not in video_db:
        return web.Response(text="Video not found", status=404)

    file_id = video_db[video_id]

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()

    file_path = data["result"]["file_path"]
    video_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

    raise web.HTTPFound(video_url)


# 🚀 App Start
app = web.Application()
app.add_routes(routes)

if __name__ == "__main__":
    web.run_app(app, port=8080)
