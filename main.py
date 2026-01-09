from __future__ import annotations
import random
import asyncio
import json
import time
import aiohttp
import os
import sys
from threading import Thread
from flask import Flask
from highrise import BaseBot, Highrise, Position, User, AnchorPosition, Item
from highrise.models import SessionMetadata
from highrise.__main__ import main, BotDefinition

class Config:
    OWNER_USERNAME = "TITOMOSTAFA"
    DEFAULT_DANCE = "dance-floss"
    DANCE_INTERVAL = 20
    HIGHRISE_ROOM_ID = os.environ.get("ROOM_ID", "691c7146253a9060fe8a2e73").strip()
    HIGHRISE_BOT_TOKEN = os.environ.get("API_TOKEN", "e9f10ca5302ab0dfd857f02d363496f3a185c3612ff9a3fc58f6cce0c762ecb0").strip()

def save_bot_position(position: dict) -> None:
    try:
        with open("bot_position.json", "w", encoding="utf-8") as f:
            json.dump(position, f)
    except: pass

def load_bot_position() -> dict | None:
    try:
        with open("bot_position.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except: return None

def save_points(points: dict) -> None:
    try:
        with open("points.json", "w", encoding="utf-8") as f:
            json.dump(points, f)
    except: pass

def load_points() -> dict:
    try:
        with open("points.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except: return {}

class Bot(BaseBot):
    def __init__(self) -> None:
        super().__init__()
        self.my_user_id: str | None = None
        self.owner_username = Config.OWNER_USERNAME
        self.current_dance = Config.DEFAULT_DANCE
        self.dancing = True
        self.saved_position = None
        self.served_drinks_count = 0
        self.points = load_points()
        self.moderators = ["TITOMOSTAFA", "", ""] 
        
        self.drinks = ["شاي", "قهوة", "عصير", "بيره", "وايت لاتيه", "بيبسي", "نسكافيه", "لبن"]
        self.drink_emojis = {"شاي": "☕", "قهوة": "☕", "عصير": "🍊", "بيره": "🍺", "بيبسي": "🥤", "لبن": "🥛"}
        
        self.random_bar_phrases = [
            "اطلب اي مشروب وانا هجهزهولك",
            "خد درينك ينسيك الاكس😂🔥", 
            "مع المنتزه   اشرب وهتنسى انت مين 🍧🔥",
            "اشرب مشروب المنتزه هتلاقي الجيار بيغينيلك 🌚♥",
            "سيبك من المزه وتعال جرب واحد شاي😂🔥",
            "البار مفتوح 24/7 🍹🔥",
            "عايز تنسى همومك؟ اطلب مشروب 😎",
            "احنا عندنا احلى المشروبات 🍺🍹",
        ]
        self.menu_phrases = ["📜 المنيو: شاي ☕ | قهوة ☕ | عصير 🍊 | بيره 🍺 | بيبسي 🥤 | نسكافيه ☕ | لبن 🥛"]

    async def get_user_id_by_username(self, username: str) -> str | None:
        try:
            api_url = f"https://create.highrise.game/api/users?username={username.strip()}"
            headers = {"User-Agent": "Mozilla/5.0"}
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as res:
                    if res.status == 200:
                        data = await res.json()
                        users_list = data.get("users", [])
                        if users_list and len(users_list) > 0:
                            return users_list[0].get("user_id")
        except: pass
        return None

    async def on_start(self, session_metadata: SessionMetadata) -> None:
        self.my_user_id = session_metadata.user_id
        self.start_time = time.time()
        print(f"🤖 البوت بدأ برقم المستخدم: {self.my_user_id}")
        
        saved_pos = load_bot_position()
        if saved_pos:
            pos = Position(saved_pos["x"], saved_pos["y"], saved_pos["z"], saved_pos.get("facing", "FrontRight"))
            try: await self.highrise.walk_to(pos)
            except: pass
        
        asyncio.create_task(self.emote_loop())
        asyncio.create_task(self.bar_phrase_loop())
        asyncio.create_task(self.menu_announcement_loop())
        asyncio.create_task(self.points_announcement_loop())
        asyncio.create_task(self.presence_points_loop())

    async def on_user_out(self, user: User) -> None:
        try:
            if user.id == self.my_user_id:
                print("🚨 البوت اتمسح من الروم! بيحاول يرجع فوراً...")
        except: pass

    async def presence_points_loop(self):
        while True:
            try:
                await asyncio.sleep(300)
                response = await self.highrise.get_room_users()
                if hasattr(response, 'content'):
                    excluded_bots = ["bot_music_almuntazah", "bot_almuntazah1", "bot_bar"]
                    for user, pos in response.content:
                        if user.id == self.my_user_id or user.username.lower() in [b.lower() for b in excluded_bots]:
                            continue
                        try:
                            priv = await self.highrise.get_room_privilege(user.id)
                            is_mod = (hasattr(priv, 'moderator') and priv.moderator) or (user.username.lower() in [m.lower() for m in self.moderators])
                            if is_mod:
                                mod_key = user.username.lower()
                                self.points[mod_key] = self.points.get(mod_key, 0) + 1
                        except: continue
                    save_points(self.points)
            except: await asyncio.sleep(10)

    async def points_announcement_loop(self):
        while True:
            await asyncio.sleep(900)
            try:
                if self.points:
                    sorted_pts = sorted(self.points.items(), key=lambda x: x[1], reverse=True)[:5]
                    msg = "🏆 ترتيب المشرفين المتصدرين حالياً:\n" + "\n".join([f"{i}. @{name} ➔ {pts} نقطة" for i, (name, pts) in enumerate(sorted_pts, 1)])
                    await self.safe_chat(msg)
            except: pass

    async def on_user_join(self, user: User, position: Position | AnchorPosition) -> None:
        try:
            priv = await self.highrise.get_room_privilege(user.id)
            is_mod = (hasattr(priv, 'moderator') and priv.moderator) or (user.username.lower() in [m.lower() for m in self.moderators])
            if is_mod:
                current_pts = self.points.get(user.username.lower(), 0)
                await self.highrise.send_whisper(user.id, f"👋 أهلاً بك @{user.username}!\n💰 رصيدك: {current_pts} نقطة")
                mod_key = user.username.lower()
                self.points[mod_key] = self.points.get(mod_key, 0) + 1
                save_points(self.points)
        except: pass

    async def on_chat(self, user: User, message: str) -> None:
        try:
            msg_l = message.strip().lower()
            username = user.username
            is_mod = any(username.lower() == mod.lower() for mod in self.moderators)

            for drink in self.drinks:
                if drink in msg_l:
                    await self.safe_chat(f"{self.drink_emojis.get(drink, '🍹')} اتفضل {drink} يا {username}!")
                    self.served_drinks_count += 1
                    return

            if msg_l == "!points" and is_mod:
                await self.safe_chat(f"👤 نقاطك يا مشرف {username}: {self.points.get(username.lower(), 0)} نقطة")
            elif msg_l == "!top":
                sorted_pts = sorted(self.points.items(), key=lambda x: x[1], reverse=True)[:5]
                await self.safe_chat("🏆 توب المشرفين:\n" + "\n".join([f"{i}. {n}: {p} نقطة" for i, (n, p) in enumerate(sorted_pts, 1)]))

            if username.lower() != self.owner_username.lower(): return

            if msg_l == "com":
                resp = await self.highrise.get_room_users()
                if hasattr(resp, 'content'):
                    for u, pos in resp.content:
                        if u.id == user.id:
                            self.saved_position = {"x": pos.x, "y": pos.y, "z": pos.z, "facing": pos.facing}
                            save_bot_position(self.saved_position)
                            await self.safe_chat("✅ تم حفظ مكان البوت.")
            elif msg_l == "you" and self.saved_position:
                await self.highrise.walk_to(Position(self.saved_position["x"], self.saved_position["y"], self.saved_position["z"]))
        except: pass

    async def safe_chat(self, message: str):
        try: await self.highrise.chat(message)
        except: pass

    async def on_error(self, message: str) -> None:
        print(f"❌ Highrise Error: {message}")
        if any(x in message.lower() for x in ["kick", "ban", "removed"]):
            print("🚨 البوت تعرض للطرد أو الحظر! سيتم إعادة التشغيل لمحاولة الدخول...")

    async def emote_loop(self):
        while True:
            try:
                if self.dancing: await self.highrise.send_emote(self.current_dance)
            except: pass
            await asyncio.sleep(Config.DANCE_INTERVAL)

    async def bar_phrase_loop(self):
        while True:
            try:
                await asyncio.sleep(random.randint(60, 120))
                await self.safe_chat(random.choice(self.random_bar_phrases))
            except: pass

    async def menu_announcement_loop(self):
        while True:
            try:
                await asyncio.sleep(random.randint(150, 200))
                await self.safe_chat(random.choice(self.menu_phrases))
            except: pass

app = Flask(__name__)
@app.route('/')
def health(): return "Bot is running"

async def run_bot():
    while True:
        try:
            print("🔄 محاولة الاتصال بالروم...")
            definitions = [BotDefinition(Bot(), Config.HIGHRISE_ROOM_ID, Config.HIGHRISE_BOT_TOKEN)]
            await main(definitions)
        except Exception as e:
            msg = str(e).lower()
            wait_time = 60 if "rate limit" in msg else 5
            print(f"🚨 خطأ: {e}. انتظار {wait_time} ثواني...")
            await asyncio.sleep(wait_time)

if __name__ == "__main__":
    Thread(target=lambda: app.run(host='0.0.0.0', port=5000), daemon=True).start()
    asyncio.run(run_bot())
