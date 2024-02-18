import pytest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_question import VoightKampff
from result import human_or_replicant
from main import add_question


def test_one_correct_answer():
    my_db = VoightKampff(db_name="test_one.db")
    add_question(my_db)

    questions_field = my_db.get_all_fields_in_questions()

    for field in questions_field:
        id = field[0]
        correct_answer = field[3]

        my_db.insert_test_result(
            id,
            correct_answer,
            13,
            60,
            6,
            4,
        )

    assert human_or_replicant(my_db) == "human"


def test_two_uncorrect_answer():
    my_db = VoightKampff(db_name="test_two.db")
    add_question(my_db)

    questions_field = my_db.get_all_fields_in_questions()

    for field in questions_field:
        id = field[0]
        correct_answer = field[3]

        my_db.insert_test_result(
            id,
            correct_answer,
            1,
            1,
            1,
            1,
        )

    assert human_or_replicant(my_db) == "replicant"


def test_three_uncorrect_answer():
    my_db = VoightKampff(db_name="test_three.db")
    add_question(my_db)

    questions_field = my_db.get_all_fields_in_questions()

    for field in questions_field:
        id = field[0]
        correct_answer = field[3]

        my_db.insert_test_result(
            id,
            correct_answer,
            -1,
            -1,
            -1,
            -1,
        )

    assert human_or_replicant(my_db) == "replicant"


def test_four_uncorrect_answer():
    my_db = VoightKampff(db_name="test_four.db")
    add_question(my_db)

    questions_field = my_db.get_all_fields_in_questions()

    for field in questions_field:
        id = field[0]
        correct_answer = field[3]

        my_db.insert_test_result(
            id,
            correct_answer,
            10000,
            10000,
            10000,
            10000,
        )

    assert human_or_replicant(my_db) == "replicant"


def test_five_correct_answer():
    my_db = VoightKampff(db_name="test_five.db")
    add_question(my_db)

    questions_field = my_db.get_all_fields_in_questions()

    for field in questions_field:
        id = field[0]
        correct_answer = field[2][0]

        my_db.insert_test_result(
            id,
            correct_answer,
            13,
            60,
            6,
            4,
        )

    assert human_or_replicant(my_db) == "replicant"


def main():
    test_one_correct_answer()
    test_two_uncorrect_answer()
    test_three_uncorrect_answer()
    test_four_uncorrect_answer()
    test_five_correct_answer()


if __name__ == "__main__":
    main()
