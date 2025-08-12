# dev_func.py
import os, json, asyncio
from telegram import Update, Bot
from telegram.ext import ContextTypes
from datetime import datetime
USERS_FILE = "tel_id.json"
NEWS_FILE  = "news.json"

def _load_json_list(path: str):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []
    return []

def load_users():
    return _load_json_list(USERS_FILE)

def load_news():
    return _load_json_list(NEWS_FILE)

async def send_news_to_all(bot: Bot):
    users = load_users()
    news_list = load_news()

    if not news_list:
        print("خبری برای ارسال نیست.")
        return

    # به هر کاربر، تک‌تک آیتم‌های خبر ارسال می‌شود
    for u in users:
        uid = u.get("user_id")
        if not isinstance(uid, int):
            continue

        n = 1
        for item in news_list:
            # اگر item دیکشنری است، شکل‌دهی متن:
            if isinstance(item, dict):
                title = item.get("title") or item.get("headline") or "خبر"
                link  = item.get("link") or item.get("url") or ""
                text = f"{title}\n{link}".strip()
            else:
                text = str(item)

            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            try:
                await bot.send_message(chat_id=uid, text=text)
                
                await bot.send_message(chat_id=uid, text=f"========{n}=={date_str}======")
                await asyncio.sleep(0.05)  # احترام به rate limit
            except Exception as e:
                if "Message is too long" in str(e):
                    # اگر پیام خیلی طولانی است، می‌توانیم آن را برش دهیم یا به چند بخش تقسیم کنیم
                    text = text[:4096]
                    await bot.send_message(chat_id=uid, text=text)
                    await bot.send_message(chat_id=uid, text=f"========{n}=={date_str}======")
                    print(f"internall send long massage for {uid} ({u.get('first_name', 'Unknown')}) : {e}")

                    await asyncio.sleep(42)  # احترام به rate limit
                else:
                    print(f"external Error for {uid} ({u.get('first_name', 'Unknown')}) : {e}")


            n = n +1

        await bot.send_message(chat_id=uid, text=f"اخبار روز {date_str} به پایان رسید ✅\nبا تشکر از شما برای استفاده از ربات ما! 🙏")
    print("all news sent to all users.")

# اگر /start نگه می‌داری:
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_first_name = update.effective_user.first_name

    data = load_users()
    if not any(u.get("user_id") == user_id for u in data):
        data.append({"user_id": user_id, "first_name": user_first_name})
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("کاربر جدید ثبت شد.")
    else:
        print("این کاربر قبلاً ثبت شده.")

    await update.message.reply_text(f"سلام {user_first_name} 👋 خوش اومدی!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ شما با موفقیت به جمع اعضای ربات پیوستید.\n"
        "📢 اخبار از منابع معتبر و به‌روز جمع‌آوری می‌شوند و به شما ارسال خواهند شد.\n"
        "⏳ لطفاً منتظر بمانید تا تازه‌ترین خبرها برایتان ارسال شود."
    )
