import random

from src.greedy import greedy_by_balas
from src.preprocesses import *
from text_coverage_data import sets_universe, wds_universe


def simulated_annealing(sets, elements, neighbourhood_scale, search_depth, print_logs=False):
    """
    Find a feasible solution for the set cover problem with greedy heuristic and optimize the solution via
    simulated annealing.

    This algorithm is the main contribution of:
        Jacobs, L. W., & Brusco, M. J. (1995). Note: A local‐search heuristic for large set‐covering problems.
        Naval Research Logistics (NRL), 42(7), 1129-1140.

    :param sets: collection of len_set_collection subsets / and a copy of it; = sets_universe (1)
    :param elements: set of words/elements to be covered.
    :param neighbourhood_scale: percentage of sets in tentative solution to be removed at each iteration; magnitude of neighbourhood-search
    :param search_depth: percentage of set cost(=length) that is accepted for new solution at each iteration; control for search-depth
    :param print_logs: prints outputs and parameters of used functions.
    :return: solution set containing a sub-collection of indices of set_collection
    """

    print("+----------------------+")
    print("| Simulated Annealing  |")
    print("+----------------------+\n")



    """
    Initialization & Pre-processes
    """

    print("Preprocesses.")
    print("Finding a feasable solution via greedy heuristic...")
    feasable_greedy_solution = greedy_by_balas(sets_universe, wds_universe, print_logs)



    print("Initialization.")
    solution_indices = set()
    not_in_solution_list = set()
    current_solution_list = get_set_list_of_solution_indices(feasable_greedy_solution)

    set_lengths = compute_set_lengths(current_solution_list)
    d = 0
    D = neighbourhood_scale * len(feasable_greedy_solution)
    E = search_depth * max(set_lengths)



    """
    Simulated Annealing
    """
    print("Solution optimization by simulated annealing approach...")

    while d != D:
        current_set = random.sample()

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
