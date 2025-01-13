import time
from typing import List, Tuple, Callable
from collections import defaultdict
from utils.extract_data_from_file import extract_data_from_file
from utils.get_list_of_lines import get_list_of_lines
from utils.SolutionResults import SolutionResults


def extract_rules_and_updates(data: List[str]) -> Tuple[List[Tuple[int, ...]], List[List[int]]]:
    split_index = next((i for i, item in enumerate(data) if "," in item), len(data))
    first_list = data[:split_index]
    second_list = data[split_index:]

    rules = [tuple(map(int, item.split("|"))) for item in first_list]
    updates = [list(map(int, item.split(","))) for item in second_list]

    return rules, updates


def create_checker_for_order(pairs: List[Tuple[int, ...]]) -> Callable[[List[int]], bool]:
    precedence: dict[int, set[int]] = defaultdict(set)
    for x, y in pairs:
        precedence[y].add(x)

    def check_order(order: List[int]) -> bool:
        position: dict[int, int] = {value: index for index, value in enumerate(order)}
        for y, dependencies in precedence.items():
            if y in order:
                for dep in dependencies:
                    if dep in order:
                        if position.get(dep, -1) > position.get(y, -1):
                            return False
        return True

    return check_order


def get_correct_updates(all_updates: List[List[int]], checker: Callable[[List[int]], bool]) -> List[List[int]]:
    correct_updates = []
    for update in all_updates:
        if checker(update):
            correct_updates.append(update)
    return correct_updates


def get_middle_elements(lists: List[List[int]]) -> List[int]:
    middle_elements = [lst[len(lst) // 2] for lst in lists if lst]
    return middle_elements


def sum_middle_elements(elements: List[int]) -> int:
    total = 0
    for element in elements:
        total += element
    return total


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(5, is_official)
    rows = get_list_of_lines(data)
    rules, updates = extract_rules_and_updates(rows)
    checker = create_checker_for_order(rules)
    correct_updates = get_correct_updates(updates, checker)
    middles = get_middle_elements(correct_updates)
    part_1 = sum_middle_elements(middles)
    part_2 = len(rows)
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(5, part_1, part_2, execution_time)
    return results
