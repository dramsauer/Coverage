import time

import numpy as np

import deterministic
from text_coverage_data import sets_universe, wds_universe


def percentage_of_solution_covering(elements, collection, solution_indices):
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
    result_str = "\nElements that actually got covered: " + str(len(solution_elements)) + \
                 "\nElements that need to get covered:  " + str(len(elements)) + \
                 "\nResulting percentage of the cover: " + str(round(percentage_overlapping*100, ndigits=3)) + "%"

    return result_str


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


    """
    Test Set from Paper
    """
    if False:
        solution_indices = deterministic.disk_friendly_greedy(test_sets_2, p=2.00, print_logs=True)
        print("\n+++++++")
        print("Solution-indices:", solution_indices)
        print("# Solution-indices:", len(solution_indices))
        solution_sets = get_set_list_of_solution_indices(test_sets_2, solution_indices)
        print("Solution-sets: ", solution_sets)
        print()
        result = percentage_of_solution_covering(wds_2, test_sets_2, solution_indices, True)
        print(result)


    """
    Final Set that is our aim to be covered
    """
    result_dict = dict()
    file = "deterministic_dfg.txt"


    for p in np.arange(1.05, 1.50, 0.05):
        f = open(file, "w")

        start = time.time()
        solution_indices = deterministic.disk_friendly_greedy(sets_universe, p, print_logs=False)
        end = time.time()
        execution_time = round(end - start, ndigits=3)

        solution_sets = get_set_list_of_solution_indices(sets_universe, solution_indices)

        percentage_str = percentage_of_solution_covering(wds_universe, sets_universe, solution_indices)

        f.write("p = " + str(p) + " >>> ")
        f.write("\nAmountof indices in solution: " + str(len(solution_indices)))
        f.write(percentage_str)
        f.write("\nTime elapsed: " + str(execution_time))
        f.write("\n\n")
        f.close()

        result_str = "\n# Solution-indices: " + str(len(solution_indices)) + percentage_str + "\nTime elapsed in sec: " + str(
            execution_time)
        print(result_str)
        result_dict[p] = result_str
        break

