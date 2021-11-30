import pytest


@pytest.mark.parametrize("expected_answer, number_passed", [(10, 5), (15, 10), (25, 20), (100, 95), (1000, 1)])
def test_addition(expected_answer, number_passed):
    actual_answer = addition(number_passed)
    assert expected_answer == actual_answer


def addition(i) -> int:
    return i+5

# To run this file open the terminal from the bottom left corner of the screen (in pycharm) and run the command
# pytest example_test.py
# (pytest {name of file}.py)
# Note that one test should fail in this example
