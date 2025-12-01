import time
from utils.extract_data_from_file import extract_data_from_file
from utils.get_list_of_lines import get_list_of_lines
from utils.SolutionResults import SolutionResults


def increment_or_decrement_number(starting_number: int, instructions: str) -> int:
    direction = instructions[0]
    magnitude = int(instructions[1:])
    result = starting_number + magnitude if direction == "R" else starting_number - magnitude
    return result


def stay_in_circle(evaluated_number: int) -> int:
    gt_max = evaluated_number > 99
    lt_min = evaluated_number < 0
    result = evaluated_number - 100 if gt_max else 100 + evaluated_number if lt_min else evaluated_number
    if result > 99 or result < 0:
        result = stay_in_circle(result)
    return result


def count_all_zeros(instructions: list[str]) -> int:
    zeroes_count = 0
    current_number = 50
    for instruction in instructions:
        initial_number = increment_or_decrement_number(current_number, instruction)
        current_number = stay_in_circle(initial_number)
        if current_number == 0:
            zeroes_count += 1
    return zeroes_count


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(1, is_official)
    instructions = get_list_of_lines(data)
    part_1 = count_all_zeros(instructions)
    part_2 = len(instructions)
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(1, part_1, part_2, execution_time)
    return results
