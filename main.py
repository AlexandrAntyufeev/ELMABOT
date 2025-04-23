
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Главное меню с эмодзи
# Главное меню с эмодзи
MAIN_MENU = ["🗂️ ЭДО", "📨 КЭДО", "📃 ДОГОВОРЫ", "🏢 КОНТРАГЕНТЫ", "🔑 ЗАБЫЛ ПАРОЛЬ ОТ СИСТЕМЫ/НЕ МОГУ ВОЙТИ"]
BACK = "⬅️ Назад"

SUBMENUS = {
    "🗂️ ЭДО": ["📝 Служебные записки", "📤 Исходящие письма", "📥 Входящие письма", BACK],
    "📨 КЭДО": ["👤 Заявка на подбор персонала", "🛠️ Выход в выходной день", "💻 Удалённая работа", "🔁 Замещения", "👶 Декрет/Увольнение/СВО", BACK],
    "📃 ДОГОВОРЫ": ["📄 Договор", "📑 Дополнительные соглашения/ПСЦ", "📋 Соглашения отдельно от договора", BACK],
    "🏢 КОНТРАГЕНТЫ": ["🏢 Контрагент", "✍️ Подписанты", BACK],
    "📝 Служебные записки": ["🆕 Создание", "✅ Согласование", "✏️ Редактирование/Корректировка", BACK],
    "📤 Исходящие письма": ["🆕 Создание", "✅ Согласование", "✏️ Редактирование/Корректировка", BACK],
    "📥 Входящие письма": ["🆕 Создание", "✅ Согласование", "✏️ Редактирование/Корректировка", BACK],
    "👤 Заявка на подбор персонала": ["🆕 Создание", "❌ Отмена", BACK],
    "🛠️ Выход в выходной день": ["🆕 Создание", BACK],
    "💻 Удалённая работа": ["🆕 Создание", "📌 Причины описание", "🔐 Настройка VPN", BACK],
    "🔁 Замещения": ["🆕 Создание", "❌ Отмена", BACK],
    "👶 Декрет/Увольнение/СВО": ["🆕 Создание", "ℹ️ Информация", BACK],
    "📄 Договор": ["🆕 Создание", "✅ Согласование", "✏️ Редактирование/Корректировка", BACK],
    "📑 Дополнительные соглашения/ПСЦ": ["🆕 Создание", "✅ Согласование", "✏️ Редактирование/Корректировка", BACK],
    "📋 Соглашения отдельно от договора": ["🆕 Создание", "✅ Согласование", "✏️ Редактирование/Корректировка", BACK],
    "🏢 Контрагент": ["🆕 Создание", "✅ Согласование", "🔄 Повторное согласование", BACK],
    "✍️ Подписанты": ["🆕 Создание", "✅ Согласование", BACK]
}

USER_STATE = {}

# Отправка клавиатуры
async def send_menu(update: Update, options):
    keyboard = [[KeyboardButton(opt)] for opt in options]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите пункт:", reply_markup=reply_markup)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USER_STATE[update.effective_user.id] = "MAIN"
    await send_menu(update, MAIN_MENU)

# Обработка навигации
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    current_state = USER_STATE.get(user_id, "MAIN")

    if text == BACK:
        if current_state in SUBMENUS:
            for parent, items in SUBMENUS.items():
                if current_state in items:
                    USER_STATE[user_id] = parent
                    return await send_menu(update, SUBMENUS[parent])
        USER_STATE[user_id] = "MAIN"
        return await send_menu(update, MAIN_MENU)

    if current_state == "MAIN" and text in SUBMENUS:
        USER_STATE[user_id] = text
        return await send_menu(update, SUBMENUS[text])

    if current_state in SUBMENUS and text in SUBMENUS.get(current_state, []):
        USER_STATE[user_id] = text
        return await send_menu(update, SUBMENUS.get(text, [BACK]))

    await update.message.reply_text(f"🔹 Информация по теме: {text}")

# Запуск
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
