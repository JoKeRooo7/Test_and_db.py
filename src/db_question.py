import sqlite3
import os

"""
Модуль для создания базы данных, для теста VoightKampff.
В нем содержится доступ к базе данных (вставка в таблицу,
получения данных из таблицы, создания таблиц).
:noindex:
"""


class VoightKampff:
    """Класс для работы с базой данных теста VoightKampff."""

    def __init__(self, db_name="voight_kampff.db"):
        """
        Инициализация объекта VoightKampff.

        Args:
            db_name (str): Имя базы данных. По умолчанию: 'voight_kampff.db'.
        """
        self.db_name = db_name
        self.db_exists = os.path.exists(self.db_name)
        self.connect_db = sqlite3.connect(self.db_name)
        self.create_or_connect_db()

    def create_or_connect_db(self):
        """
        Подключение к существующей базе данных или её создание.

        Returns:
            sqlite3.Connection: Объект подключения к базе данных.
        """
        if not self.db_exists:
            self.create_tables()
        return self.connect_db

    def create_tables(self):
        """Создание таблицы в базе данных"""
        cursor = self.connect_db.cursor()  # Указатель на бд
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                question TEXT,
                options TEXT,
                correct_answer TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_result (
                id INTEGER PRIMARY KEY,
                question_id INTEGER,
                answer TEXT,
                breath INTEGER,
                pulse INTEGER,
                redness_level INTEGER,
                pupil_dilation INTEGER
            )
        ''')
        self.connect_db.commit()

    def insert_question(self, question, options, correct_answer):
        """
        Вставка вопроса в базу данных

        :param question: Вопрос.
        :param options: Варианты ответа.
        :param correct_answer: Верный вариант ответа
        """
        cursor = self.connect_db.cursor()
        cursor.execute('''
            INSERT INTO questions (question, options, correct_answer)
            VALUES (?, ?, ?)
        ''', (question, ', '.join(options), correct_answer))
        self.connect_db.commit()

    def insert_test_result(self, question_id, answer, breath, pulse,
                           redness_level, pupil_dilation):
        """
        Вставка ответов в базу данныых

        :param question_id: Идентификатор вопроса.
        :param answer: Ответ на вопрос.
        :param breath: Количество вздохов за 1 минуту.
        :param pulse: ЧСС за 1 минуту.
        :param redness_level: Уровень покраснения (от 1 до 6).
        :param pupil_dilation: Расширение зрачка.
        """
        cursor = self.connect_db.cursor()
        cursor.execute('''
            INSERT INTO test_result
            (question_id, answer, breath, pulse, redness_level, pupil_dilation)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (question_id, answer, breath, pulse, redness_level,
              pupil_dilation))
        self.connect_db.commit()

    def check_question(self, question):
        """
        Проверка на существование вопроса

        :param question: Вопрос который надо проверить.
        """
        cursor = self.connect_db.cursor()
        cursor.execute("SELECT * FROM questions WHERE question = ?",
                       (question,))
        result = cursor.fetchone()
        return result

    def get_all_fields_in_questions(self):
        """
        Функция для возврата всех полей таблицы questions

        :return: Вовзрат всех полей таблицы questions
        """
        cursor = self.connect_db.cursor()
        cursor.execute('''
        SElECT * FROM questions
        ''')
        all_field = cursor.fetchall()
        return all_field

    def get_all_fields_in_test_result(self):
        """
        Функция для возврата всех полей таблицы test_result

        :return: Вовзрат всех полей таблицы test_result
        """
        cursor = self.connect_db.cursor()
        cursor.execute('''
        SElECT * FROM test_result
        ''')
        all_field = cursor.fetchall()
        return all_field

    def clear_table(self):
        """
        Функция для удаления всех таблиц
        """
        cursor = self.connect_db.cursor()
        cursor.execute('''
            DROP TABLE IF EXISTS questions
        ''')
        cursor.execute('''
            DROP TABLE IF EXISTS test_result
        ''')
        self.connect_db.commit()

    def close_connection(self):
        """
        Закрыть соединение с бд
        """
        self.connect_db.close()
