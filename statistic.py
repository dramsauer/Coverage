import random
from copy import deepcopy

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

    feasable_greedy_solution = greedy(sets_universe, wds_universe)

    solution_indices = set()


    return solution_indices


def greedy(sets, elements):
    """
    Find a feasible solution for the set cover problem with greedy heuristic.
    :param sets: collection of sets; with set_collection as a copy of it
    :param elements: set of words/elements to be covered; with words_to_cover as a copy of it
    :return: solution set containing a sub-collection of indices of set_collection
    """


    """
    Initialization & Pre-processes
    """


    print("Initialization.")

    set_collection = deepcopy(sets)
    words_to_cover = list(deepcopy(elements))
    amount_words = len(words_to_cover)

    solution_indices = set()

    # 1. Select randomly one of the words, that need to be covered
    random_word = words_to_cover[random.randint(0, amount_words)]

    # 2. Select first set
    for set in set_collection:
        # If the random word is part of the current chosen set,
        # then add the index of the set to solution_indices
        if random_word in set:
            print(random_word)
            print(set_collection.index(set))
            solution_indices.add(set_collection.index(set))
            break

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

    solution = simulated_annealing(sets_universe, wds_universe, print_logs=False)
    # solution = simulated_annealing(test_sets_2, wds_2, print_logs=False)
    #print("\n+++++++")
    #print("Solution:")
    #print(solution)

    # #solution = simulated_annealing(sets_universe, wds_universe, print_logs=False)
    # solution = simulated_annealing(test_sets_2, wds_2, print_logs=False)
    #print("\n+++++++")
    #print("Solution:")
    #print(solution)

