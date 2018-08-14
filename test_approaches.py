import deterministic
from text_coverage_data import sets_universe


def percentage_of_solution_covering(elements, collection, solution_indices, print_details=False):
    """
    Method for verifying whether a solution-index-set contains the same elements
    as the reference elements list or not and therefore represents an optimal solution.
    :param elements: elements that need to be covered
    :param collection: collection of sets for covering
    :param solution_indices: containing indices of sets covered from collection
    :return: percentage value how many elements the solution elements cover
    """
    solution_elements = set()
    for i in solution_indices:
        for j in collection[i]:
            solution_elements.add(j)
    percentage_overlapping = len(solution_elements) / len(elements)
    if print_details:
        print("Elements that need to get covered:  ", elements)
        print("Elements that actually got covered: ", solution_elements)

    return percentage_overlapping


def get_set_list_of_solution_indices(collection, solution_indices):
    sets = list()
    for i in solution_indices:
        sets.append(collection[i])
    return sets


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

    # solution = disk_friendly_greedy(sets_universe, p=1.05, print_logs=True)
    solution_indices = deterministic.disk_friendly_greedy(test_sets_2, p=2.00, print_logs=True)
    print("\n+++++++")
    print("Solution-indices:", solution_indices)
    print("# Solution-indices:", len(solution_indices))
    solution_sets = get_set_list_of_solution_indices(test_sets_2, solution_indices)
    print("Solution-sets: ", solution_sets)
    print()
    print("# Elements that need to get covered: ", len(wds_2))
    result = percentage_of_solution_covering(wds_2, test_sets_2, solution_indices)
    print("Result - are all elements covered by solution: ", result)
