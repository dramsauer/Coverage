import deterministic
import statistic
from text_coverage_data import wds_universe, sets_universe


def verify_solution(elements, collection, solution_indices):
    """
    Method for verifying whether a solution-index-set contains the same elements
    as the reference elements list or not and therefore represents an optimal solution.
    :param elements: elements that need to be covered
    :param collection: collection of sets for covering
    :param solution_indices: containing indices of sets covered from collection
    :return: boolean value if solution covers elements
    """
    solution_elements = set()
    for i in solution_indices:
        for j in collection[i]:
            solution_elements.add(j)
    print("Elements that need to get covered:  ", elements)
    print("Elements that actually got covered: ", solution_elements)
    return elements == solution_elements


if __name__ == "__main__":
    print("")

    """
    Execution of the disk-friendly greedy algorithm &
    for the given set cover problem.
    The set collection is contained in sets_universe,
    the elements to cover are stored in wds_universe.

    2 Test sets are also prepared further down.
    """


    # Test set containing only a partition of sets_universe:
    test_sets_1 = [sets_universe[0],
                   sets_universe[1],
                   sets_universe[2],
                   sets_universe[3],
                   sets_universe[5],
                   sets_universe[6],
                   sets_universe[7],
                   sets_universe[8],
                   sets_universe[9]
                   ]
    # Test set containing sets as in the paper example and the corresponding wds universe:
    test_sets_2 = [
        {'A', 'B', 'C', 'D', 'E'},
        {'A', 'B', 'D', 'F', 'G'},
        {'A', 'F', 'G'},
        {'B', 'C', 'G'},
        {'G', 'H'},
        {'E', 'H'},
        {'C', 'I'},
        {'A'},
        {'E'},
        {'I'}
                   ]
    wds_2 = {
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'
    }

    # solution = disk_friendly_greedy(wds_universe, sets_universe, p=2, print_logs=TRUE)
    solution_indices = deterministic.disk_friendly_greedy(wds_2, test_sets_2, p=2, print_logs=False)
    print("\n+++++++")
    print("Solution-indices:", solution_indices)
    result = verify_solution(wds_2, test_sets_2, solution_indices)
    print("Result - are all elements covered by solution: ", result)
