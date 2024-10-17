"""
Telegram-бот для генерації API токенів

Цей скрипт реалізує Telegram-бота, який виконує наступні функції:
1. Створення бази даних SQLite для зберігання інформації про користувачів.
2. Запит імені користувача.
3. Запит та валідація email адреси користувача.
4. Генерація унікального API токену для користувача.
5. Збереження даних користувача (ім'я, email, API токен) в базі даних.
6. Збереження історії чату користувача.

Принцип роботи:
1. Запит імені від користувача. (#1)
   - Бот надсилає повідомлення з проханням ввести ім'я.
2. Запит пошти від користувача. (#2)
   - Бот надсилає повідомлення з проханням ввести email.
3. Перевірка формату email. (#3)
   - Валідація введеної пошти для запобігання некоректним значенням.
4. Генерація унікального API токену. (#4)
   - Якщо пошта коректна, генерується унікальний токен за допомогою UUID.
5. Збереження даних користувача. (#5)
   - Ім'я, пошта та згенерований токен зберігаються в базі даних.
6. Відправка API токену користувачу. (#6)
   - Бот надсилає користувачу повідомлення з його унікальним токеном.
7. Обробка помилок, якщо пошта вже існує в базі. (#7)
   - Повідомляється, що пошта вже зареєстрована, і пропонується ввести іншу.
8. Збереження історії чату. (#8)
   - Кожне повідомлення користувача зберігається в базі даних як частина історії чату.

"""

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3
import re
import uuid

def create_db():
    """
    Створює базу даних SQLite та таблицю користувачів, якщо вони ще не існують.
    """
    conn = sqlite3.connect('telegram_users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT NOT NULL UNIQUE,
                        api_token TEXT UNIQUE,
                        name TEXT,
                        conversation_history TEXT)''')
    conn.commit()
    conn.close()
    print("База даних успішно створена або вже існує")

# Виконуємо створення бази даних
create_db()

def generate_api_token():
    """
    Генерує унікальний API токен за допомогою UUID.
    
    Returns:
        str: Унікальний API токен.
    """
    return str(uuid.uuid4())

def is_valid_email(email):
    """
    Перевіряє, чи є введений email коректним.
    
    Args:
        email (str): Email для перевірки.
    
    Returns:
        bool: True, якщо email коректний, False в іншому випадку.
    """
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обробляє команду /start, розпочинаючи діалог з користувачем.
    
    Args:
        update (Update): Об'єкт оновлення Telegram.
        context (ContextTypes.DEFAULT_TYPE): Контекст бота.
    """
    await update.message.reply_text('Привіт! Будь ласка, введіть ваше ім\'я.')
    context.user_data['step'] = 'name'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обробляє повідомлення від користувача залежно від поточного кроку діалогу.
    
    Args:
        update (Update): Об'єкт оновлення Telegram.
        context (ContextTypes.DEFAULT_TYPE): Контекст бота.
    """
    step = context.user_data.get('step', 'name')
    
    if step == 'name':  # #1 Запит імені користувача
        name = update.message.text
        context.user_data['name'] = name
        await update.message.reply_text(f'Дякую, {name}! Тепер, будь ласка, введіть вашу електронну пошту.')
        context.user_data['step'] = 'email'
    elif step == 'email':  # #2 Запит пошти від користувача
        email = update.message.text
        if is_valid_email(email):  # #3 Перевірка формату email
            api_token = generate_api_token()  # #4 Генерація унікального API токену
            name = context.user_data.get('name', 'Невідомий')
            try:
                conn = sqlite3.connect('telegram_users.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (email, api_token, name, conversation_history) VALUES (?, ?, ?, ?)',
                               (email, api_token, name, ''))  # #5 Збереження даних користувача
                conn.commit()
                conn.close()
                await update.message.reply_text(f'Ваш API токен: {api_token}')  # #6 Відправка API токену
                context.user_data['step'] = 'chat'
                context.user_data['email'] = email
            except sqlite3.IntegrityError:  # #7 Обробка помилок
                await update.message.reply_text('Ця пошта вже зареєстрована. Використайте іншу.')
        else:
            await update.message.reply_text('Невірний формат пошти. Будь ласка, спробуйте ще раз.')
    elif step == 'chat':  # #8 Збереження історії чату
        message = update.message.text
        email = context.user_data.get('email')
        conn = sqlite3.connect('telegram_users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT conversation_history FROM users WHERE email = ?', (email,))
        result = cursor.fetchone()
        if result:
            history = result[0]
            new_history = f'{history}, "{message}"' if history else f'"{message}"'
            cursor.execute('UPDATE users SET conversation_history = ? WHERE email = ?', (new_history, email))
            conn.commit()
        conn.close()
        await update.message.reply_text('Повідомлення збережено.')

def main():
    """
    Основна функція для запуску бота.
    """
    application = ApplicationBuilder().token("7738669556:AAEvBO67BN34za5MoCByyVuxP1YrSr85iac").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()

"""
Пояснення щодо генерації API токену:

У коді для генерації API токену використовується алгоритм UUID (Universally Unique Identifier). 
Це стандартний спосіб створення унікальних ідентифікаторів, який забезпечує велику ймовірність 
того, що згенеровані токени будуть унікальними.

Принцип UUID:
1. Унікальність: UUID генерується таким чином, що ймовірність отримання однакового значення
   в різних системах є вкрай низькою. Це досягається шляхом використання випадкових значень,
   часу, а також інформації про мережеві адреси.
2. Стандарт: UUID відповідає стандарту RFC 4122, який визначає формат UUID і способи його генерації.
   Стандарт описує кілька версій UUID, які можуть базуватися на різних джерелах інформації
   (випадкові числа, час тощо).
3. Зручність: Завдяки простоті та надійності, UUID широко використовується в різних сферах,
   включаючи бази даних, API, системи управління контентом тощо.

Генерація в коді:
У коді це реалізовано за допомогою стандартної бібліотеки Python:

import uuid

def generate_api_token():
    return str(uuid.uuid4())

Функція uuid.uuid4() генерує випадковий UUID (версія 4), що забезпечує унікальність з високою ймовірністю.
"""