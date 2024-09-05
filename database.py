import aiosqlite, ast

DB_NAME_DEFAULT = 'quiz_bot.db'

async def create_table(db_name=DB_NAME_DEFAULT):
    # Создаем соединение с базой данных (если она не существует, то она будет создана)
    async with aiosqlite.connect(db_name) as db:
        # Выполняем SQL-запрос к базе данных
        await db.execute('CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER DEFAULT 0, score INTEGER DEFAULT 0)')
        # Сохраняем изменения
        await db.commit()

async def update_quiz_index(user_id, index, db_name=DB_NAME_DEFAULT):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(db_name) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        # Сохраняем изменения
        await db.commit()

async def get_quiz_index(user_id, db_name=DB_NAME_DEFAULT):
     # Подключаемся к базе данных
     async with aiosqlite.connect(db_name) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

async def update_score(user_id, score, db_name=DB_NAME_DEFAULT):
    async with aiosqlite.connect(db_name) as db:
        print(await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, score) VALUES (?, ?)', (user_id, score)))
        # Сохраняем измененияx
        await db.commit()
    
async def get_score(user_id, db_name=DB_NAME_DEFAULT):
     # Подключаемся к базе данных
     async with aiosqlite.connect(db_name) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT score FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

async def get_stats(db_name=DB_NAME_DEFAULT):
    # Подключаемся к базе данных
     async with aiosqlite.connect(db_name) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT user_id, score FROM quiz_state ORDER BY score DESC') as cursor:
            # Возвращаем результат
            results = await cursor.fetchall()
            if results is not None:
                return dict(ast.literal_eval(str(results)))
            else:
                return {}