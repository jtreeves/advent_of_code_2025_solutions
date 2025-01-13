import time
from typing import List, Tuple, Callable
from collections import defaultdict, deque
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


def get_correct_and_incorrect_updates(all_updates: List[List[int]], checker: Callable[[List[int]], bool]) -> Tuple[List[List[int]], List[List[int]]]:
    correct_updates = []
    incorrect_updates = []
    for update in all_updates:
        if checker(update):
            correct_updates.append(update)
        else:
            incorrect_updates.append(update)
    return correct_updates, incorrect_updates


# def correct_order_with_kahns(pairs: List[Tuple[int, ...]], unordered_list: List[int]) -> List[int]:
#     precedence: dict[int, set[int]] = defaultdict(set)
#     in_degree: dict[int, int] = defaultdict(int)

#     for x, y in pairs:
#         precedence[y].add(x)
#         in_degree[x] += 1
#         if x not in in_degree:
#             in_degree[x] = 0
#         if y not in in_degree:
#             in_degree[y] = 0

#     zero_in_degree = deque([node for node in unordered_list if in_degree[node] == 0])
#     sorted_order = []

#     while zero_in_degree:
#         node = zero_in_degree.popleft()
#         if node in unordered_list:
#             sorted_order.append(node)

#             for neighbor in precedence[node]:
#                 in_degree[neighbor] -= 1
#                 if in_degree[neighbor] == 0:
#                     zero_in_degree.append(neighbor)

#     print("SORTED ORDER:", sorted_order)
#     return sorted_order


def correct_order(incorrect_list: List[int], check_order: Callable[[List[int]], bool]) -> List[int]:
    if check_order(incorrect_list):
        return incorrect_list

    for i in range(len(incorrect_list) - 1):
        incorrect_list[i], incorrect_list[i + 1] = incorrect_list[i + 1], incorrect_list[i]
        result = correct_order(incorrect_list[:], check_order)

        if check_order(result):
            return result

        incorrect_list[i], incorrect_list[i + 1] = incorrect_list[i + 1], incorrect_list[i]

    return []


def correct_all_incorrect_updates(incorrect_updates: List[List[int]], check_order: Callable[[List[int]], bool]) -> List[List[int]]:
    corrected_updates = []
    for update in incorrect_updates:
        corrected_updates.append(correct_order(update, check_order))
    return corrected_updates


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
    correct_updates, incorrect_updates = get_correct_and_incorrect_updates(updates, checker)
    print("INCORRECT UPDATES:", incorrect_updates)
    middles = get_middle_elements(correct_updates)
    corrected_updates = correct_all_incorrect_updates(incorrect_updates, checker)
    middles_for_incorrect_updates = get_middle_elements(corrected_updates)
    part_1 = sum_middle_elements(middles)
    part_2 = sum_middle_elements(middles_for_incorrect_updates)
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(5, part_1, part_2, execution_time)
    return results
