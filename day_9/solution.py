import time
from utils.extract_data_from_file import extract_data_from_file
from utils.get_list_of_lines import get_list_of_lines
from utils.SolutionResults import SolutionResults


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(9, is_official)
    rows = get_list_of_lines(data)
    part_1 = len(rows)
    part_2 = len(rows)
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(9, part_1, part_2, execution_time)
    return results
