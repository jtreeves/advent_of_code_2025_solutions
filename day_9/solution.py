import time
from typing import List
from utils.extract_data_from_file import extract_data_from_file
from utils.SolutionResults import SolutionResults


def parse_disk_map(disk_map: str) -> List[str]:
    blocks = []
    file_id = 0
    is_file = True

    for _, char in enumerate(disk_map):
        length = int(char)
        if is_file:
            blocks.extend([str(file_id)] * length)
            file_id += 1
        else:
            blocks.extend(['.'] * length)
        is_file = not is_file

    return blocks


def move_blocks_to_fill_gaps(blocks: List[str]) -> List[str]:
    result = blocks[:]

    for i in range(len(result) - 1, -1, -1):
        if result[i] != '.':
            for j in range(len(result)):
                if result[j] == '.':
                    if j < i:
                        result[j], result[i] = result[i], '.'
                    break

    return result


def calculate_checksum(blocks: List[str]) -> int:
    return sum(pos * int(block) for pos, block in enumerate(blocks) if block != '.')


def compact_and_checksum(disk_map: str) -> int:
    blocks = parse_disk_map(disk_map)
    compacted_blocks = move_blocks_to_fill_gaps(blocks)
    checksum = calculate_checksum(compacted_blocks)
    return checksum


def solve_problem(is_official: bool) -> SolutionResults:
    start_time = time.time()
    data = extract_data_from_file(9, is_official)
    part_1 = compact_and_checksum(data)
    part_2 = 2
    end_time = time.time()
    execution_time = end_time - start_time
    results = SolutionResults(9, part_1, part_2, execution_time)
    return results
