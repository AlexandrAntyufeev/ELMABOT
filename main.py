
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

BACK = "⬅️ Назад"

USER_STATE = {}

# Ответы с краткой справкой и изображением
RESPONSES = {
    "📄 Договор: 🆕 Создание": {
        "text": "Нажмите кнопку +Договор. Заполните обязательные поля (*), затем нажмите Сохранить и отправьте на согласование.",
        "image": "dogovor_create.png"
    },
    "📑 Дополнительные соглашения/ПСЦ: 🆕 Создание": {
        "text": "Нажмите +Доп. соглашение. Заполните все обязательные поля (*), прикрепите файл, выберите форму и сохраните.",
        "image": "psc_card.png"
    },
    "📋 Соглашение отдельно от договора: 🆕 Создание": {
        "text": "Нажмите +Соглашение. Укажите контрагента, тип соглашения, заполните обязательные поля (*) и сохраните.",
        "image": "agreement_separate.png"
    },
    "🏢 Контрагент: 🆕 Создание": {
        "text": "Нажмите +Контрагент. Укажите ИНН или название, заполните все обязательные поля (*), сохраните и отправьте на согласование.",
        "image": "contractor_create.png"
    }
}

# Главный экран
MAIN_MENU = list(set(k.split(":")[0] for k in RESPONSES.keys()))

# Навигация
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USER_STATE[update.effective_user.id] = "MAIN"
    keyboard = [[KeyboardButton(item)] for item in MAIN_MENU]
    await update.message.reply_text("Выберите раздел:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == BACK:
        USER_STATE[user_id] = "MAIN"
        keyboard = [[KeyboardButton(item)] for item in MAIN_MENU]
        await update.message.reply_text("Возврат в главное меню:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        return

    current_state = USER_STATE.get(user_id, "MAIN")

    # Первая навигация вглубь
    if current_state == "MAIN" and any(k.startswith(text) for k in RESPONSES):
        USER_STATE[user_id] = text
        options = [k.split(":")[1].strip() for k in RESPONSES if k.startswith(text)]
        keyboard = [[KeyboardButton(option)] for option in options] + [[KeyboardButton(BACK)]]
        await update.message.reply_text(f"Раздел: {text}. Выберите пункт:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        return

    # Ответ по справке
    full_key = f"{current_state}: {text}"
    if full_key in RESPONSES:
        resp = RESPONSES[full_key]
        await update.message.reply_text(resp["text"])
        try:
            with open(f"images/{resp['image']}", "rb") as img:
                await update.message.reply_photo(photo=InputFile(img))
        except Exception:
            await update.message.reply_text("⚠️ Картинка пока не прикреплена.")
        return

    await update.message.reply_text("Извините, я не понял. Нажмите /start для начала.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
