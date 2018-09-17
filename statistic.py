import random
from copy import deepcopy

from preprocesses import *
from text_coverage_data import sets_universe, wds_universe


def simulated_annealing(sets, elements, print_logs=False):
    """
    Find a feasible solution for the set cover problem with greedy heuristic.
    :param sets: collection of len_set_collection subsets / and a copy of it; = sets_universe (1)
    :param elements: set of words/elements to be covered.
    :param print_logs: prints outputs and parameters of used functions.
    :return: solution set containing a sub-collection of indices of set_collection
    """

    print("+----------------------+")
    print("| Simulated Annealing  |")
    print("+----------------------+\n")



    """
    Initialization & Pre-processes
    """


    print("Initialization.")
    print("Finding a feasable solution via greedy heuristic...")
    feasable_greedy_solution = greedy(sets_universe, wds_universe, print_logs)

    solution_indices = set()


    return solution_indices


def greedy(sets, elements, print_logs=False):
    """
    Find a feasible solution for the set cover problem with greedy heuristic.
    :param sets: collection of sets; with set_collection as a copy of it
    :param elements: set of words/elements to be covered; with words_to_cover as a copy of it
    :param print_logs: prints outputs and parameters of used functions.
    :return: solution set containing a sub-collection of indices of set_collection
    """
    print()
    print("+------------------+")
    print("| Greedy Heuristic |")
    print("+------------------+\n")


    """
    Initialization & Pre-processes
    """

    print("\nInitialization.")

    set_collection = deepcopy(sets)
    sorted_collection, comparison_dict = sort_collection_by_set_sizes_with_comparison_dict(set_collection)

    words_to_cover = list(deepcopy(elements))
    amount_words = len(words_to_cover)

    solution_indices = list()

    """
    Main-Algorithm
    """

    print("\nLoop.")
    print("Iterating over all words that need to get covered...")

    # Iterating over all words that need to get covered (= step 3 in paper also)
    while amount_words > 0:
        # 1. Select randomly one of the words
        random_word = words_to_cover[random.randint(0, amount_words)]

        # 2. Select first set in natural order
        for set in sorted_collection:
            # If the random word is part of the current chosen set,
            # then add the index of the set to solution_indices
            if random_word in set:
                original_set_index = comparison_dict.get(sorted_collection.index(set))
                solution_indices.append(original_set_index)

                break
        words_to_cover.remove(random_word)
        amount_words -= 1
    # 4. Remove redundant entries in list by saving it as a set
    solution_indices = set(solution_indices)

    if print_logs:
        print("Amount of indices in Greedy-Solution: ", len(solution_indices))
    return solution_indices


if __name__ == "__main__":
    print("")

    """
    Execution of the the simulated annealing algorithm for the given set cover problem.
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

    solution = simulated_annealing(sets_universe, wds_universe, print_logs=True)
    # solution = simulated_annealing(test_sets_2, wds_2, print_logs=False)
    #print("\n+++++++")
    #print("Solution:")
    #print(solution)

    # #solution = simulated_annealing(sets_universe, wds_universe, print_logs=False)
    # solution = simulated_annealing(test_sets_2, wds_2, print_logs=False)
    #print("\n+++++++")
    #print("Solution:")
    #print(solution)
