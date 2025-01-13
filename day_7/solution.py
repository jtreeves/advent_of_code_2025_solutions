import time
from typing import List
from itertools import product
from utils.extract_data_from_file import extract_data_from_file
from utils.get_list_of_lines import get_list_of_lines
from utils.SolutionResults import SolutionResults


def generate_combinations(total_numbers: int) -> List[List[str]]:
    return [list(comb) for comb in product(["+", "*"], repeat=total_numbers - 1)]


def evaluate_expression(numbers: List[int], operators: List[str]) -> int:
    result = numbers[0]
    for i in range(1, len(numbers)):
        if operators[i - 1] == "+":
            result += numbers[i]
        elif operators[i - 1] == "*":
            result *= numbers[i]
    return result


def check_if_target_possible(description: str) -> bool:
    target_str, numbers_str = description.split(":")
    target = int(target_str.strip())
    numbers = list(map(int, numbers_str.strip().split()))
    operator_combinations = generate_combinations(len(numbers))
    for operators in operator_combinations:
        if evaluate_expression(numbers, operators) == target:
            return True
    return False


def get_all_successful_targets(descriptions: List[str]) -> List[int]:
    successful_targets = []
    for description in descriptions:
        if check_if_target_possible(description):
            successful_targets.append(int(description.split(":")[0].strip()))
    return successful_targets


def sum_successful_targets(successful_targets: List[int]) -> int:
    total = 0
    for target in successful_targets:
        total += target
    return total


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(7, is_official)
    rows = get_list_of_lines(data)
    successful_targets = get_all_successful_targets(rows)
    part_1 = sum_successful_targets(successful_targets)
    part_2 = len(rows)
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(7, part_1, part_2, execution_time)
    return results
