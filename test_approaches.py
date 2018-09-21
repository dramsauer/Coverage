import os
import time

from src.disk_friendly_greedy import *
from src.simulated_annealing import *
from src.greedy import *
from src.preprocesses import *
from text_coverage_data import sets_universe, wds_universe
import numpy as np
import pickle

# from src import disk_friendly_greedy, greedy, preprocesses


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
    # print("wds: ", wds_universe.__class__)
    # print("sets: ", sets_universe.__class__)

    """
    Execution of the disk-friendly-greedy algorithm &
    simulated-annealing algorithm
    for the given set cover problem.
    The set collection is contained in sets_universe,
    the elements to cover are stored in wds_universe.

    """

    # Testing the Disk-Friendly-Greedy
    if False:

        headline = "p,Amount of sets in solution,Covered Elements,Elements to be covered,Coverage Rate,Sum of all Set-sizes in solution,Time elapsed in sec\n"

        file = "out/disk_friendly_greedy_results.csv"
        f = open(file, "a")
        if os.stat(file).st_size == 0:
            f.write(headline)

        for p in np.arange(1.005, 2.000, 0.005):
            start = time.time()
            solution_indices = disk_friendly_greedy(sets=sets_universe,
                                                    p=round(p, ndigits=4),
                                                    print_logs=False)
            end = time.time()

            execution_time = round(end - start, ndigits=3)
            solution_indices_len = len(solution_indices)
            solution_len, elements_len, percentage = percentage_of_solution_covering(wds_universe, sets_universe,
                                                                                     solution_indices)
            solution_sets = get_set_list_of_solution_indices(sets_universe, solution_indices)
            solution_sets_sizes = get_sum_of_all_set_sizes_of_solution_indices(sets_universe, solution_indices)

            values = str(round(p, ndigits=4)) + "," + str(solution_indices_len) + "," + str(solution_len) + "," + str(
                elements_len) + "," + str(percentage) + "," + str(solution_sets_sizes) + "," + str(execution_time) + "\n"
            print(headline)
            print(values)
            f.write(values)

        f.close()

    # Testing the greedy_by_balas heuristic
    if False:
        headline = "Amount of sets in solution,Covered Elements,Elements to be covered,Coverage Rate,Sum of all Set-sizes in solution,,Time elapsed in sec\n"

        file = "out/greedy_results.csv"
        f = open(file, "a")
        if os.stat(file).st_size == 0:
            f.write(headline)

        for i in range(50):
            start = time.time()
            solution_indices = greedy_by_balas(sets=sets_universe,
                                               elements=wds_universe,
                                               print_logs=True)
            end = time.time()

            execution_time = round(end - start, ndigits=3)
            solution_indices_len = len(solution_indices)
            solution_len, elements_len, percentage = percentage_of_solution_covering(wds_universe, sets_universe,
                                                                                     solution_indices)
            solution_sets = get_set_list_of_solution_indices(sets_universe, solution_indices)
            solution_sets_sizes = get_sum_of_all_set_sizes_of_solution_indices(sets_universe, solution_indices)

            print(headline)
            values = str(solution_indices_len) + "," + str(solution_len) + "," + str(elements_len) + "," + str(
                percentage) + "," + str(solution_sets_sizes) + "," + str(execution_time) + "\n"
            print(values)
            f.write(values)

    # Saving a greedy solution as pickle file (good for testing simulated annealing)
    if False:
        (greedy_solution_indices, greedy_coverage_matrix) = greedy_by_balas_with_coverage_matrix(sets=sets_universe, elements=wds_universe, print_logs=True)

        with open('save_solution.p', 'wb') as fp:
            pickle.dump((greedy_solution_indices, greedy_coverage_matrix), fp)

    # Testing the simulated annealing
    if True:
        headline = "Amount of sets in solution,Covered Elements,Elements to be covered,Coverage Rate,Time elapsed in sec\n"

        file = "out/simulated_annealing_results.csv"
        f = open(file, "a")
        if os.stat(file).st_size == 0:
            f.write(headline)

        if os.stat('save_solution.p').st_size == 0:
            (greedy_solution_indices, greedy_coverage_matrix) = greedy_by_balas_with_coverage_matrix(sets=sets_universe, elements=wds_universe, print_logs=True)
            with open('save_solution.p', 'wb') as fp:
                pickle.dump((greedy_solution_indices, greedy_coverage_matrix), fp)

        with open('save_solution.p', 'rb') as fp:
            (greedy_solution_indices, greedy_coverage_matrix) = pickle.load(fp)


        # for p1 in np.arange(0.05, 0.2, 0.05):
        for i in range(1):
            time_limit = 60
            start = time.time()
            solution_indices = simulated_annealing(sets=sets_universe,
                                                   predefined_solution=greedy_solution_indices,
                                                   amount_elements_covered_dict=greedy_coverage_matrix,
                                                   running_time=time_limit,
                                                   print_logs=True)
            end = time.time()
            execution_time = round(end - start, ndigits=3)

            solution_indices_len = len(solution_indices)
            solution_len, elements_len, percentage = percentage_of_solution_covering(wds_universe, sets_universe,
                                                                                     solution_indices)

            print(headline)
            values = str(solution_indices_len) + "," + str(solution_len) + "," + str(elements_len) + "," + str(
                percentage) + "," + str(execution_time) + "\n"
            print(values)
            f.write(values)
