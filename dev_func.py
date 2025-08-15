# dev_func.py
import os, json, asyncio
from telegram import Update, Bot , ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes ,MessageHandler, filters
from translator import traslator
import jdatetime
from datetime import datetime
USERS_FILE = "tel_id.json"
NEWS_FILE_BTC  = "news_BTC.json"
tres = traslator()



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

def load_newsBTC():
    return _load_json_list(NEWS_FILE_BTC)


async def send_news_to_all_BTC(bot: Bot):
    users = load_users()
    news_list = load_newsBTC()

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
            now_sh = jdatetime.datetime.now()
            date_str_sh = now_sh.strftime("%Y-%m-%d")
            weekdays = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یک‌شنبه"]
            day_name = weekdays[now.weekday()]
            full_date = f"{day_name} {date_str}"
            try:
                text = tres.en_to_fa(text)
                await bot.send_message(chat_id=uid, text=text)
                await bot.send_message(chat_id=uid, text=f"=== {n} === {full_date} ===")
                await asyncio.sleep(42)  # احترام به rate limit
            except Exception as e:
                if "Message is too long" in str(e):
                    # اگر پیام خیلی طولانی است، می‌توانیم آن را برش دهیم یا به چند بخش تقسیم کنیم
                    text = text[:4096]
                    text = tres.en_to_fa(text)
                    await bot.send_message(chat_id=uid, text=text)
                    await bot.send_message(chat_id=uid, text=f"=== {n} === {full_date} ===")
                    print(f"internall send long massage for {uid} ({u.get('first_name', 'Unknown')}) : {e}")

                    await asyncio.sleep(42)  # احترام به rate limit
                else:
                    print(f"external Error for {uid} ({u.get('first_name', 'Unknown')}) : {e}")


            n = n +1

        await bot.send_message(chat_id=uid, text=f"اخبار روز {date_str} به پایان رسید ✅\nبا تشکر از شما برای استفاده از ربات ما! 🙏")
    print("all news sent to all users.")


def build_main_keyboard():
    # ـــ ردیف‌ها را مثل ماتریس تعریف کن؛ هر ردیف یک لیست از دکمه‌ها
    keyboard_layout = [
        ["اخبار BTC 📈"],
    ]
    return ReplyKeyboardMarkup(
        keyboard_layout,
        resize_keyboard=True,   # ـــ کیبورد فشرده
        one_time_keyboard=False # ـــ باز بماند
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ـــ ذخیره عضو جدید
    user_id = update.effective_user.id
    user_first_name = update.effective_user.first_name
    data = load_users()

    if not any(isinstance(u, dict) and u.get("user_id") == user_id for u in data):
        data.append({"user_id": user_id, "first_name": user_first_name})
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"join {user_id} ({user_first_name})")
    else:
        print(f"subscriber {user_id} ({user_first_name})")

    # ـــ پیام خوش‌آمد + کیبورد اصلی
    await update.message.reply_text(
        f"سلام {user_first_name} 👋 خوش اومدی!",
        reply_markup=build_main_keyboard()
    )

async def send_btc_news(chat_id, bot):
    uid = chat_id
    news_list = load_newsBTC()
    n = 1
    for item in news_list:
        if isinstance(item, dict):
            title = item.get("title") or item.get("headline") or "خبر"
            link  = item.get("link") or item.get("url") or ""
            text = f"{title}\n{link}".strip()
        else:
            text = str(item)

            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            now_sh = jdatetime.datetime.now()
            date_str_sh = now_sh.strftime("%Y-%m-%d")
            weekdays = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یک‌شنبه"]
            day_name = weekdays[now.weekday()]
            full_date = f"{day_name} {date_str}"
            try:
                text = tres.en_to_fa(text)
                await bot.send_message(chat_id=uid, text=text[:4095])
                await bot.send_message(chat_id=uid, text=f"=== {n} === {full_date} ===")
                await asyncio.sleep(0.03)  # احترام به rate limit
            except Exception as e:
                if "Message is too long" in str(e):
                    text = text[:4095]
                    text = tres.en_to_fa(text)
                    await bot.send_message(chat_id=uid, text=text)
                    await bot.send_message(chat_id=uid, text=f"=== {n} === {full_date} ===")
                    print(f"internall send long massage for {uid} ({uid('first_name', 'Unknown')}) : {e}")

                    await asyncio.sleep(0.03)  # احترام به rate limit
                else:
                    print(f"external Error for {uid} ({uid('first_name', 'Unknown')}) : {e}")
        n = n +1

        if n > 5:
            break
    await bot.send_message(chat_id=uid, text=f"اخبار روز {date_str} به پایان رسید ✅\nبا تشکر از شما برای استفاده از ربات ما! 🙏")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_massage = (update.message.text or "").strip()
    user_id = update.effective_user.id
    user_first_name = update.effective_user.first_name
    user_data = context.user_data

    if user_massage == "اخبار BTC 📈":
        await update.message.reply_text(
        "5 خبر از آخرین اخبار BTC در حال ارسال است...\nلطفاً صبر کنید.",
        reply_markup=build_main_keyboard()
        )
        await send_btc_news(update.effective_chat.id, context.bot)

        return

    await update.message.reply_text(
        "✅ شما با موفقیت به جمع اعضای ربات پیوستید.\n"
        "📢 اخبار از منابع معتبر و به‌روز جمع‌آوری می‌شوند و به شما ارسال خواهند شد.\n"
        "⏳ لطفاً منتظر بمانید تا تازه‌ترین خبرها برایتان ارسال شود.",
        reply_markup=build_main_keyboard()
    )
