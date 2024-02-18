import db_question as db

"""
Модуль с результатом и логикой проверки на человека и репликанта
:noindex:
"""

need_procent = 0.7


def check_answer(row, answer) -> bool:
    """
    Функция для проверки ответа

    :param row: строка вопроса с ответом.
    :param answer: ответ на вопрос
    :return: True, если ответ на вопрос совпадает с правильным.
    """

    if row[3].rstrip() == answer.rstrip():
        return True
    else:
        return False


def check_breath(breath) -> bool:
    """
    Функция для проверки дыхания 12-16 вздохов в минуту

    :param breath: количества вздохов
    :return: True, если количество вздохов в
        минуту удовлетворяет тест Войта-Кампфа
    """
    if breath < 17 and breath > 11:
        return True
    else:
        return False


def check_pulse(pulse) -> bool:
    """
    Функция для проверки пульса от 60 до 100 чсс в минуту

    :param pulse: пульс чсс
    :return: True, чсс в минуту удовлетворяет тест Войта-Кампфа
    """
    if pulse < 101 and pulse > 59:
        return True
    else:
        return False


def check_redness_level(redness_level) -> bool:
    """
    Функция для проверки уровня покрасения 6 возможных уровней

    :param redness_level: уровень покраснения
    :return: True, если уровень покраснения в пределах теста Войта-Кампфа
    """
    if redness_level < 7:
        return True
    else:
        return False


def check_pupil_dilation(pupil_dilation) -> bool:
    """
    Функция для проверки уровня расширения зрачка, от 2 до 8мм

    :param pupil_dilation: расширения зрачка
    :return: True, если  расширения зрачка в пределах теста Войта-Кампфа
    """
    if pupil_dilation < 9 and pupil_dilation > 1:
        return True
    else:
        return False


def human_or_replicant(database=db.VoightKampff()):
    """
    Функция для проверки на репликанта

    :param database: Название базы данных. По умолчанию класс VoightKampff()
    :return: "human" если более 70% ответов правильны и 70% показателей тоже
    """
    true_answer = 0
    false_answer = 0
    true_indicators = 0
    false_indicators = 0

    my_db = database
    questions_field = my_db.get_all_fields_in_questions()
    result_field = my_db.get_all_fields_in_test_result()

    if not questions_field:
        print("Вопросов нет =(")
        return None

    for result in result_field:
        row = questions_field[result[1] - 1]
        if check_answer(row, result[2]):
            true_answer += 1
        else:
            false_answer += 1

        if (
            check_breath(result[3]) and
            check_pulse(result[4]) and
            check_redness_level(result[5]) and
            check_pupil_dilation(result[6])
           ):
            true_indicators += 1
        else:
            false_indicators += 1

        # print("-", true_answer, ' : ' , false_answer)
        # print("--", true_indicators, ' : ' , false_indicators)

    if true_answer / (true_answer + false_answer) < need_procent:
        return "replicant"

    if true_indicators / (true_indicators + false_indicators) < need_procent:
        return "replicant"

    return "human"


if __name__ == "__main__":
    print(human_or_replicant())
