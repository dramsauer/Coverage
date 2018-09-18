import time

import disk_friendly_greedy
import statistic
from text_coverage_data import sets_universe, wds_universe


def percentage_of_solution_covering(elements, collection, solution_indices):
    """
    Method for verifying whether a solution-index-set contains the same elements
    as the reference elements list or not and therefore represents an optimal solution.
    :param elements: elements that need to be covered
    :param collection: collection of sets for covering
    :param solution_indices: containing indices of sets covered from collection
    :return: amount of solution elements, amount elements to cover and
             percentage value how many elements are covered by the solution elements
    """
    solution_elements = set()
    for i in solution_indices:
        for j in collection[i]:
            solution_elements.add(j)
    percentage_overlapping = len(solution_elements) / len(elements)

    return len(solution_elements), len(elements), percentage_overlapping



def testing_on_example_data():
    global solution_indices
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

    solution_indices = disk_friendly_greedy.disk_friendly_greedy(test_sets_2, p=2.00, print_logs=True)
    print("\n+++++++")
    print("Solution-indices:", solution_indices)
    print("# Solution-indices:", len(solution_indices))
    solution_sets = get_set_list_of_solution_indices(test_sets_2, solution_indices)
    print("Solution-sets: ", solution_sets)
    print()
    result = percentage_of_solution_covering(wds_2, test_sets_2, solution_indices, True)
    print(result)


if __name__ == "__main__":
    print("")
    # testing_on_example_data()

    """
    Execution of the disk-friendly greedy algorithm &
    for the given set cover problem.
    The set collection is contained in sets_universe,
    the elements to cover are stored in wds_universe.

    """

    # Testing the Disk-Friendly-Greedy
    if False:

        headline = "p,Amount of sets in solution,Covered Elements,Elements to be covered,Coverage Rate,Time elapsed in sec\n"

        file = "results/deterministic_dfg_results.csv"
        f = open(file, "a")
        f.write(headline)

        for p in np.arange(1.005, 2.000, 0.005):
            start = time.time()
            solution_indices = deterministic.disk_friendly_greedy(sets_universe, round(p, ndigits=4), print_logs=False)
            end = time.time()

            execution_time = round(end - start, ndigits=3)
            solution_indices_len = len(solution_indices)
            solution_len, elements_len, percentage = percentage_of_solution_covering(wds_universe, sets_universe, solution_indices)
            # solution_sets = get_set_list_of_solution_indices(sets_universe, solution_indices)

            values = str(round(p, ndigits=4)) + "," + str(solution_indices_len) + "," + str(solution_len) + "," + str(elements_len) + "," + str(percentage) + "," + str(execution_time) + "\n"
            print(headline)
            print(values)
            f.write(values)

        f.close()

    # Testing the greedy heuristic
    if True:
        headline = "Iteration,Amount of sets in solution,Covered Elements,Elements to be covered,Coverage Rate,Time elapsed in sec\n"

        file = "results/greedy_results.csv"
        f = open(file, "a")
        f.write(headline)

        for i in range(10):
            start = time.time()
            solution_indices = statistic.greedy(sets_universe, wds_universe, True)
            end = time.time()

            execution_time = round(end - start, ndigits=3)
            solution_indices_len = len(solution_indices)
            solution_len, elements_len, percentage = percentage_of_solution_covering(wds_universe, sets_universe, solution_indices)
            # solution_sets = get_set_list_of_solution_indices(sets_universe, solution_indices)

            print(headline)
            values = str(i) + "," + str(solution_indices_len) + "," + str(solution_len) + "," + str(elements_len) + "," + str(percentage) + "," + str(execution_time) + "\n"
            print(values)
            f.write(values)
