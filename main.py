import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

BACK = "⬅️ Назад"

USER_STATE = {}

# Ответы с краткой справкой и изображением
RESPONSES = {
    # Главное меню
    "📑 ЭДО": {
        "text": "Выберите раздел:",
        "image": "edo_image.png"
    },
    "📄 Договоры": {
        "text": "Выберите действие с договором:",
        "image": "dogovor_image.png"
    },
    "📑 КЭДО": {
        "text": "Выберите действие в КЭДО:",
        "image": "kedo_image.png"
    },
    "🏢 Контрагенты": {
        "text": "Выберите действие с контрагентами:",
        "image": "kontargent_image.png"
    },
    "👤 Подписанты": {
        "text": "Выберите действия с подписантом:",
        "image": "podpisant_image.png"
    },

    # ЭДО
    "📑 ЭДО: 📝 Служебные записки": {
        "text": "Выберите действие с служебными записками:",
        "image": "service_note.png"
    },
    "📑 ЭДО: 📤 Исходящие письма": {
        "text": "Выберите действие с исходящими письмами:",
        "image": "outgoing_mail.png"
    },
    "📑 ЭДО: 📥 Входящие письма": {
        "text": "Выберите действие с входящими письмами:",
        "image": "incoming_mail.png"
    },

    # Договоры
    "📄 Договоры: 📄 Договор": {
        "text": "Нажмите кнопку +Договор. Заполните обязательные поля (*), затем нажмите Сохранить и отправьте на согласование.",
        "image": "dogovor_create.png"
    },
    "📄 Договоры: 📑 ДС": {
        "text": "Заполните данные для договора с учетом ДС и отправьте на согласование.",
        "image": "ds_create.png"
    },
    "📄 Договоры: 📜 ПСЦ": {
        "text": "Заполните поля ПСЦ и отправьте на согласование.",
        "image": "psc_create.png"
    },
    "📄 Договоры: 📋 Соглашения": {
        "text": "Нажмите кнопку +Соглашение, выберите контрагента и сохраните.",
        "image": "agreement_create.png"
    },

    # КЭДО
    "📑 КЭДО: 💻 Удалёнка": {
        "text": "Действия с удалёнкой для сотрудников.",
        "image": "remote_work.png"
    },
    "📑 КЭДО: 📝 Заявка на подбор персонала": {
        "text": "Заявка на подбор персонала.",
        "image": "staff_request.png"
    },

    # Контрагенты
    "🏢 Контрагенты: 🏢 Создание": {
        "text": "Нажмите +Контрагент. Укажите ИНН или название и сохраните.",
        "image": "contractor_create.png"
    },
    "🏢 Контрагенты: ✅ Согласование": {
        "text": "Начните процесс согласования с контрагентом.",
        "image": "contractor_approval.png"
    },

    # Подписанты
    "👤 Подписанты: Подписание": {
        "text": "Подписать документы с контрагентом.",
        "image": "sign_document.png"
    },
    "👤 Подписанты: Подписано с обеих сторон": {
        "text": "Документ подписан обеими сторонами.",
        "image": "signed_document.png"
    },
    
    # Карточка договора
    "📄 Договор: Карточка договора": {
        "text": "При переходе в карточку договора пользователь видит основную информацию по договору, все доступные вкладки и кнопки действий с документом.",
        "image": "kartochka.png"
    },
    "📄 Договор: Карточка договора: Запросить регистрацию": {
        "text": "Запросить регистрацию – используется для запроса присвоения регистрационного номера документу до окончания согласования.",
        "image": "registration_request.png"
    },
    "📄 Договор: Карточка договора: Редактировать частично": {
        "text": "Редактировать частично – используется для корректировки несущественных атрибутов документа без прерывания процесса согласования.",
        "image": "partial_edit.png"
    },
    "📄 Договор: Карточка договора: Редактировать и прервать согласование": {
        "text": "Редактировать и прервать согласование – используется для редактирования всего документа, данное действие прервёт процесс согласования договора и вернёт договор инициатору для корректировки.",
        "image": "edit_and_interrupt_approval.png"
    },

    # Согласование
    "📄 Договор: ✅ Согласование": {
        "text": "Для типовой формы договора система автоматически генерирует шаблон договора и выбирает шаблон процесса согласования в соответствии с закрепленными и утвержденными маршрутами в системе...",
        "image": "agreement_approval.png"
    },
    "📄 Договор: 📝 Рассмотрение": {
        "text": "При выборе инициатором нетиповой формы договора после запуска процесса выбирается шаблон процесса в зависимости от выбранного типа договора...",
        "image": "agreement_review.png"
    },
    "📄 Договор: Подписание": {
        "text": "После того, как получены все согласования от всех ответственных отделов (учитывая согласования с комментариями), назначается задача на подписание документа...",
        "image": "sign_order.png"
    },
    "📄 Договор: Подписано с обеих сторон": {
        "text": "Если документ уже подписан со стороны контрагента, то инициатор получит задачу по подписанию с обеих сторон.",
        "image": "signed_contract.png"
    }
}

# Главный экран
MAIN_MENU = [
    "📑 ЭДО", "📄 Договоры", "📑 КЭДО", "🏢 Контрагенты", "👤 Подписанты"
]

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
