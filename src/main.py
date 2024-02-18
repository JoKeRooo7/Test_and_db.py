import db_question as db
import questions as q
from result import human_or_replicant

"""
Модуль для взаимосвязи между базоый данных и пользовательским интерфейсом
:noindex:
"""

my_db = db.VoightKampff()


def add_question(database):
    """
    Добавляет вопросы в базу данных.

    :param database: Экземпляр базы данных.
    """
    database.clear_table()
    database.create_tables()
    for test in q.TEST_QUESTION:
        question = test["question"]

        if not database.check_question(question):
            options = test["options"]
            correct_answer = test["correct_answer"]

            database.insert_question(question, options,
                                     correct_answer)


def validate_input(value, min_val, max_val):
    """
    Проверяет корректность введенных данных.

    :param value: Введенное значение.
    :param min_val: Минимальное допустимое значение.
    :param max_val: Максимальное допустимое значение.
    :return: True, если введенные данные верны, иначе False.
    """
    if value.isdigit():
        int_value = int(value)
        if min_val <= int_value <= max_val:
            return True

    print("Введите корректные данные")
    return False


def check_answer(answer, options):
    """
    Проверяет корректность ответа на вопрос.

    :param answer: Ответ на вопрос.
    :param options: Возможнын ответы на вопрос.
    :return: True, если введенные данные корректны, иначе False.
    """
    if answer.isdigit() and 1 <= int(answer) <= len(options):
        return True
    elif answer.rstrip() in options:
        return True
    else:
        print(
            "Данного варианта ответа не существует."
            "Введите корректные данные"
            )
        return False


def input_in_db(field):
    """
    Вставляет введенные пользователем данные в базу данных

    :param field: Строка из базы данных, содержит id, вопрос,
        ответы на вопрос, правильный ответ.
    """
    id, question, options = field[:3]
    options_list = options.split(', ')

    print(question)
    for option in options_list:
        print(f" * {option}")

    answer = None
    breath = None
    pulse = None
    redness_level = None
    pupil_dilation = None

    print("Выберите один из вариантов:")
    answer = input().rstrip('\n,.')

    while not check_answer(answer, options_list):
        answer = input().rstrip('\n,.')

    print("Количество дыханий в минуту:")
    breath = input()
    while not validate_input(breath, 1, 50):
        breath = input()

    print("ЧСС за 60 секунд:")
    pulse = input()
    while not validate_input(pulse, 1, 200):
        pulse = input()

    print("Уровень покраснения:")
    print(" 1: Отсутствует")
    print(" 2: Слабое")
    print(" 3: Умеренное")
    print(" 4: Среднее")
    print(" 5: Сильное")
    print(" 6: Критическое")
    print(" 7: Иной")
    print("Выберите вариант в цифрах:")
    redness_level = input()

    while not validate_input(redness_level, 1, 7):
        redness_level = input()

    print("Расширение зрачка в мм:")
    pupil_dilation = input()
    while not validate_input(pupil_dilation, 1, 10):
        pupil_dilation = input()

    my_db.insert_test_result(id, answer, breath, pulse,
                             redness_level, pupil_dilation)


def main():
    """
    Запускает программу для ответов на вопрос
    """
    all_field = my_db.get_all_fields_in_questions()

    print("============---- Тест на репликанта ----============")

    for field in all_field:
        input_in_db(field)


if __name__ == "__main__":
    add_question(my_db)

    if not my_db.get_all_fields_in_questions():
        print("Вопросов нет =(")
    else:
        main()
        print(human_or_replicant(my_db))
        my_db.close_connection()
