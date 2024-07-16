import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext

# Встановлення логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ваш API ключ TMDb
TMDB_API_KEY = '752d7c973cdd047502ebdb61b48cfae7'

# Словники для збереження виборів користувачів
user_preferences = {}

# Словник для відповідності жанрів TMDb
GENRES = {
    'historical': 36,
    'action': 28,
    'western': 37,
    'war': 10752,
    'detective': 9648,
    'documentary': 99,
    'drama': 18,
    'horror': 27,
    'comedy': 35,
    'crime': 80,
    'melodrama': 10749,
    'music': 10402,
    'animation': 16,
    'adventure': 12,
    'family': 10751,
    'tv_movie': 10770,
    'thriller': 53,
    'science_fiction': 878,
    'fantasy': 14
}

# Функція для команди /start
async def start(update: Update, context: CallbackContext) -> None:
    welcome_message = (
        "Привіт! Я твій бот для вибору фільмів. "
        "Я допоможу тобі знайти фільм за твоїм смаком. "
        "Щоб почати, будь ласка, вибери жанр фільму з наведених нижче."
    )
    
    keyboard = [
        [InlineKeyboardButton("Історичний", callback_data='genre_historical'), InlineKeyboardButton("Бойовик", callback_data='genre_action'), InlineKeyboardButton("Вестерн", callback_data='genre_western')],
        [InlineKeyboardButton("Військовий", callback_data='genre_war'), InlineKeyboardButton("Детектив", callback_data='genre_detective'), InlineKeyboardButton("Документальний", callback_data='genre_documentary')],
        [InlineKeyboardButton("Драма", callback_data='genre_drama'), InlineKeyboardButton("Жахи", callback_data='genre_horror'), InlineKeyboardButton("Комедія", callback_data='genre_comedy')],
        [InlineKeyboardButton("Кримінал", callback_data='genre_crime'), InlineKeyboardButton("Мелодрама", callback_data='genre_melodrama'), InlineKeyboardButton("Музика", callback_data='genre_music')],
        [InlineKeyboardButton("Мультфільм", callback_data='genre_animation'), InlineKeyboardButton("Пригоди", callback_data='genre_adventure'), InlineKeyboardButton("Сімейний", callback_data='genre_family')],
        [InlineKeyboardButton("Телефільм", callback_data='genre_tv_movie'), InlineKeyboardButton("Трилер", callback_data='genre_thriller'), InlineKeyboardButton("Фантастика", callback_data='genre_science_fiction')],
        [InlineKeyboardButton("Фентезі", callback_data='genre_fantasy')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    query_data = query.data.split('_')
    category = query_data[0]
    selection = query_data[1]

    user_id = query.from_user.id

    if category == 'genre':
        user_preferences[user_id] = {'genre': selection}
        keyboard = [
            [InlineKeyboardButton("Українська", callback_data='language_uk')],
            [InlineKeyboardButton("Англійська", callback_data='language_en')],
            [InlineKeyboardButton("Корейська", callback_data='language_ko')],
            [InlineKeyboardButton("Китайська", callback_data='language_zh')],
            [InlineKeyboardButton("Німецька", callback_data='language_de')],
            [InlineKeyboardButton("Французька", callback_data='language_fr')],
            [InlineKeyboardButton("Польська", callback_data='language_pl')],
            [InlineKeyboardButton("Чеська", callback_data='language_cs')],
            [InlineKeyboardButton("Японська", callback_data='language_ja')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Ви обрали жанр: {selection}\nТепер виберіть мову озвучки:", reply_markup=reply_markup)
    elif category == 'language':
        user_preferences[user_id]['language'] = selection
        keyboard = [
            [InlineKeyboardButton(str(year), callback_data=f'year_{year}') for year in range(1990, 1995)],
            [InlineKeyboardButton(str(year), callback_data=f'year_{year}') for year in range(1995, 2000)],
            [InlineKeyboardButton(str(year), callback_data=f'year_{year}') for year in range(2000, 2005)],
            [InlineKeyboardButton(str(year), callback_data=f'year_{year}') for year in range(2005, 2010)],
            [InlineKeyboardButton(str(year), callback_data=f'year_{year}') for year in range(2010, 2015)],
            [InlineKeyboardButton(str(year), callback_data=f'year_{year}') for year in range(2015, 2020)],
            [InlineKeyboardButton(str(year), callback_data=f'year_{year}') for year in range(2020, 2025)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"Ви обрали мову озвучки: {selection}\nТепер виберіть рік випуску фільму:", reply_markup=reply_markup)
    elif category == 'year':
        user_preferences[user_id]['year'] = selection
        preferences = user_preferences[user_id]
        recommendation, image_url, rating = await get_movie_recommendation(preferences)
        if image_url:
            await query.message.reply_photo(photo=image_url, caption=f"Ви обрали рік випуску: {selection}\nРекомендований фільм: {recommendation}\nВікове обмеження: {rating}")
        else:
            await query.edit_message_text(text=f"Ви обрали рік випуску: {selection}\nРекомендований фільм: {recommendation}\nВікове обмеження: {rating}")

        # Додана кнопка для завершення і продовження
        keyboard = [
            [InlineKeyboardButton("Замовити квитки", url="https://t5wisvdljy2rrgoqofhzow.on.drv.tw/%D0%9F%D1%80%D0%B0%D0%BA%D1%82%D0%B8%D0%BA%D0%B0/%D0%9E%D1%81%D0%BD%D0%BE%D0%B2%D0%BD%D0%B0/%D0%9F%D1%80%D0%B5%D0%BC'%D1%94%D1%80%D0%B0/%D0%A4%D1%96%D0%BB%D1%8C%D0%BC%D0%B8/%D0%A1%D0%B5%D0%B0%D0%BD%D1%81%D0%B8/%D0%9A%D0%B2%D0%B8%D1%82%D0%BA%D0%B8/%D0%91%D1%80%D0%BE%D0%BD%D1%8E%D0%B2%D0%B0%D0%BD%D0%BD%D1%8F%20%D0%BA%D0%B2%D0%B8%D1%82%D0%BA%D0%B0.html")],
            [InlineKeyboardButton("Продовжити", callback_data='restart_language')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Що бажаєте зробити далі?", reply_markup=reply_markup)
    elif category == 'restart':
        # Очищення виборів користувача
        user_preferences.pop(user_id, None)
        # Видалення повідомлення про підтвердження
        await query.message.delete()
        
        # Виведення вибору жанру фільму знову
        welcome_message = (
            "Будь ласка, вибери жанр фільму з наведених нижче."
        )
        keyboard = [
            [InlineKeyboardButton("Історичний", callback_data='genre_historical'), InlineKeyboardButton("Бойовик", callback_data='genre_action'), InlineKeyboardButton("Вестерн", callback_data='genre_western')],
            [InlineKeyboardButton("Військовий", callback_data='genre_war'), InlineKeyboardButton("Детектив", callback_data='genre_detective'), InlineKeyboardButton("Документальний", callback_data='genre_documentary')],
            [InlineKeyboardButton("Драма", callback_data='genre_drama'), InlineKeyboardButton("Жахи", callback_data='genre_horror'), InlineKeyboardButton("Комедія", callback_data='genre_comedy')],
            [InlineKeyboardButton("Кримінал", callback_data='genre_crime'), InlineKeyboardButton("Мелодрама", callback_data='genre_melodrama'), InlineKeyboardButton("Музика", callback_data='genre_music')],
            [InlineKeyboardButton("Мультфільм", callback_data='genre_animation'), InlineKeyboardButton("Пригоди", callback_data='genre_adventure'), InlineKeyboardButton("Сімейний", callback_data='genre_family')],
            [InlineKeyboardButton("Телефільм", callback_data='genre_tv_movie'), InlineKeyboardButton("Трилер", callback_data='genre_thriller'), InlineKeyboardButton("Фантастика", callback_data='genre_science_fiction')],
            [InlineKeyboardButton("Фентезі", callback_data='genre_fantasy')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(welcome_message, reply_markup=reply_markup)
    elif category == 'restart_language':
        # Видалення повідомлення про підтвердження
        await query.message.delete()

        # Виведення вибору мови озвучки фільму знову
        keyboard = [
            [InlineKeyboardButton("Українська", callback_data='language_uk')],
            [InlineKeyboardButton("Англійська", callback_data='language_en')],
            [InlineKeyboardButton("Корейська", callback_data='language_ko')],
            [InlineKeyboardButton("Китайська", callback_data='language_zh')],
            [InlineKeyboardButton("Німецька", callback_data='language_de')],
            [InlineKeyboardButton("Французька", callback_data='language_fr')],
            [InlineKeyboardButton("Польська", callback_data='language_pl')],
            [InlineKeyboardButton("Чеська", callback_data='language_cs')],
            [InlineKeyboardButton("Японська", callback_data='language_ja')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Хочете обрати мову озвучки?", reply_markup=reply_markup)

async def get_movie_recommendation(preferences: dict) -> tuple:
    genre = preferences['genre']
    language = preferences['language']
    year = preferences['year']

    # Відправляємо запит до TMDb API
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&language={language}&with_genres={GENRES[genre]}&primary_release_year={year}"
    response = requests.get(url)
    data = response.json()

    if 'results' in data and len(data['results']) > 0:
        movie = data['results'][0]
        title = movie['title']
        overview = movie['overview']
        poster_path = movie['poster_path']
        image_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else None

        # Отримуємо вікове обмеження для фільму
        movie_id = movie['id']
        rating_url = f"https://api.themoviedb.org/3/movie/{movie_id}/release_dates?api_key={TMDB_API_KEY}"
        rating_response = requests.get(rating_url)
        rating_data = rating_response.json()

        rating = "Невідомо"
        for country in rating_data['results']:
            if country['iso_3166_1'] == 'US':
                if country['release_dates']:
                    rating = country['release_dates'][0]['certification']
                break

        return f"\nНазва: {title}\nОпис: {overview}", image_url, rating
    else:
        return "На жаль, не знайшов фільмів за вашими запитами", None, "Невідомо"

async def finish(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_preferences.pop(user_id, None)
    await update.message.reply_text("Натисніть /start щоб розпочати з початку.")

def main() -> None:
    application = Application.builder().token("7271813592:AAG_NgEK6gCsGgy3TFWWShY-rXr4nhCMC_8").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("finish", finish))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
