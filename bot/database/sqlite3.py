import sqlite3
import time

from bot.data.settings import PATH_DATABASE
from bot.utils.logger import logger

class Database:
    def __init__(self, db_file: str):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        logger.info(f"База данных была успешна подключена [{PATH_DATABASE}]...")

    def __del__(self):
        """Закрываем соединение при уничтожении объекта."""
        self.conn.close()

    ############################## Общие методы ##############################

    def fetch_one(self, query: str, params: tuple) -> tuple | None:
        """Возвращает одну запись."""
        return self.cursor.execute(query, params).fetchone()

    def fetch_all(self, query: str, params: tuple = ()) -> list[tuple]:
        """Возвращает все записи."""
        return self.cursor.execute(query, params).fetchall()

    def execute(self, query: str, params: tuple) -> None:
        """Выполняет запрос без возврата результата."""
        self.cursor.execute(query, params)
        self.conn.commit()

    def record_exists(self, query: str, params: tuple) -> bool:
        """Проверяет существование записи."""
        result = self.fetch_one(query, params)
        return result is not None

    ############################## Таблица users ##############################

    def get_all_users(self) -> list[tuple]:
        return self.fetch_all("SELECT * FROM `users`")

    def user_exists(self, user_id: int) -> bool:
        return self.record_exists("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))

    def get_user_param(self, user_id: int, param: str) -> any:
        result = self.fetch_one(f"SELECT `{param}` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result[0] if result else None

    def update_user_param(self, user_id: int, param: str, value: any) -> None:
        self.execute(f"UPDATE `users` SET `{param}` = ? WHERE `user_id` = ?", (value, user_id))

    def add_user(self, user_id: int, **kwargs) -> int:
        """Добавляет пользователя в таблицу users."""
        columns = ['user_id'] + list(kwargs.keys()) + ['created_at']
        placeholders = ', '.join(['?'] * len(columns))
        values = (user_id, *kwargs.values(), time.time())
        self.execute(f"INSERT INTO `users` ({', '.join(columns)}) VALUES ({placeholders})", values)
        return self.cursor.lastrowid
    
    ############################## Таблица logs ##############################

    def add_log_entry(self, user_id: int, message: str, action: str, **kwargs) -> int:
        columns = ['user_id', 'message', 'action'] + list(kwargs.keys()) + ['created_at']
        placeholders = ', '.join(['?'] * len(columns))
        values = (user_id, message, action, *kwargs.values(), time.time())
        self.execute(f"INSERT INTO `logs` ({', '.join(columns)}) VALUES ({placeholders})", values)
        return self.cursor.lastrowid

    def get_latest_log_entry(self, conditions: dict):
        """
        Возвращает последнюю запись из таблицы logs, удовлетворяющую условиям.
        
        :param conditions: Словарь с условиями для фильтрации (column: value).
        :return: Последняя запись в виде словаря или None, если запись не найдена.
        """
        if not conditions:
            raise ValueError("Необходимо указать хотя бы одно условие.")

        where_clause = " AND ".join([f"`{key}` = ?" for key in conditions.keys()])
        query = f"""
            SELECT *
            FROM `logs`
            WHERE {where_clause}
            ORDER BY `created_at` DESC
            LIMIT 1
        """

        result = self.cursor.execute(query, tuple(conditions.values())).fetchone()

        if result:
            columns = [desc[0] for desc in self.cursor.description]
            return dict(zip(columns, result))
        return None

logger.info(f"Начинаю подключение к базе данных [{PATH_DATABASE}]...")
db = Database(PATH_DATABASE)
