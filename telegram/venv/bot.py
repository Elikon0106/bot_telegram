from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import openai
import logging

# Настройки токенов и API
API_TOKEN = 'YPT'  # Замените на ваш токен
OPENAI_API_KEY = 'YOAK'  # Замените на ваш OpenAI API ключ
openai.api_key = OPENAI_API_KEY

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Список курсов с видеоматериалами и заданиями
courses = [
    {
        "name": "Python для начинающих",
        "description": "Изучите основы программирования на Python.",
        "video_link": "https://www.youtube.com/watch?v=34Rp6KVGIEM&list=PLDyJYA6aTY1lPWXBPk0gw6gR8fEtPDGKa",
        "assignment_link": "https://forms.gle/GycAscHsMpsf4fbm7"
    },
    {
        "name": "Основы машинного обучения",
        "description": "Погружение в мир машинного обучения.",
        "video_link": "https://www.youtube.com/watch?v=n9SZNtzdS00&list=PLEwK9wdS5g0rFDizykiWLVzeH0rsCQSTM",
        "assignment_link": "https://forms.gle/dARrKE4MeYYc29ry5"
    },
    {
        "name": "SQL и базы данных",
        "description": "Основы работы с SQL и проектирования баз данных.",
        "video_link": "https://www.youtube.com/watch?v=uGKIXTUjZbc&list=PLtPJ9lKvJ4oh5SdmGVusIVDPcELrJ2bsT",
        "assignment_link": "https://forms.gle/JHNQhNVSudFgncsK7"
    },
    {
        "name": "Product Manager",
        "description": "Продукты и их разивитие.",
        "video_link": "https://www.youtube.com/watch?v=OyXaYYh5Nm0&list=PLrCZzMib1e9o-y5T-G0l94eqeKYnC01H4",
        "assignment_link": "https://forms.gle/JFiRPRkUNECUezh7A"
    },
    {
        "name": "Язык программирования C++/C#",
        "description": "Изучите основы программирования на C++ и C#.",
        "video_link": "https://www.youtube.com/watch?v=_8yZYhAkQjQ&list=PLDyJYA6aTY1laYPs6iS-SrYl9DZLVCUKr",
        "assignment_link": "https://forms.gle/WXrnsc8wXWjtq5Bb9"
    },
    {
        "name": "Язык программирования Go",
        "description": "Изучите основы программирования на языке Go.",
        "video_link": "https://www.youtube.com/watch?v=xoz-Y9T8gRc&list=PLgG7lPwNdp57aUoqLpR0Rk7Q5v4dFHsjg",
        "assignment_link": "https://forms.gle/atRnzhHUJ62cavMZ8"
    }
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}! Добро пожаловать в нашу Платформу Innowacja. Введите /help для получения списка команд.",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Команды:\n/start - Начать\n/help - Помощь\n/courses - Список курсов")

async def send_courses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton(course['name'], callback_data=course['name'])] for course in courses]
    keyboard.append([InlineKeyboardButton("Назад", callback_data='back')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите курс:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == 'back':
        await send_courses(update, context)
        return
    selected_course = next((course for course in courses if course['name'] == query.data), None)
    if selected_course:
        await query.edit_message_text(text=f"Вы выбрали курс: {selected_course['name']}\n"
                                            f"Описание: {selected_course['description']}\n"
                                            f"Ссылка на видео: {selected_course['video_link']}\n"
                                            f"Ссылка на задание: {selected_course['assignment_link']}")

def main():
    app = ApplicationBuilder().token(API_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("courses", send_courses))
    app.add_handler(CallbackQueryHandler(button))

    try:
        logger.info("Бот запущен...")
        app.run_polling()
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
