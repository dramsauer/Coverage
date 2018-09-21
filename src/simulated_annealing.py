import random
from collections import defaultdict
from copy import deepcopy

from src.greedy import greedy_by_balas_with_coverage_matrix
from src.preprocesses import *
from text_coverage_data import sets_universe


def simulated_annealing(sets, elements, neighbourhood_scale, search_depth, predefined_solution=None, print_logs=False):
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
    :param predefined_solution: for multiple iterations of testing you can give this method a feasable solution to start with
    :param print_logs: prints outputs and parameters of used functions.
    :return: solution set containing a sub-collection of indices of set_collection
    """

    """
    Initialization & Pre-processes
    """
    set_collection = deepcopy(sets)

    if predefined_solution is None:
        if print_logs:
            print("Preprocesses.")
            print("Finding a feasable solution via greedy heuristic...")
        feasable_greedy_solution, amount_elements_covered_dict = greedy_by_balas_with_coverage_matrix(sets=set_collection, elements=elements, print_logs=print_logs)
    else:
        feasable_greedy_solution, amount_elements_covered_dict = predefined_solution

    #for iteration in iterations:
    solution_indices = local_search_heuristic(set_collection, elements, neighbourhood_scale, search_depth, feasable_greedy_solution, amount_elements_covered_dict, print_logs)

    #solution_indices = set()

    return solution_indices



def local_search_heuristic(sets, elements, neighbourhood_scale, search_depth, solution, amount_elements_covered_dict, print_logs=False):
    """
    This algorithm is the main contribution of:
        Jacobs, L. W., & Brusco, M. J. (1995). Note: A local‐search heuristic for large set‐covering problems.
        Naval Research Logistics (NRL), 42(7), 1129-1140.

    :param amount_elements_covered_dict: a dict which saves the numbers, how often each element is covered
    :param sets: collection of len_set_collection subsets / and a copy of it; = sets_universe
    :param elements: set of words/elements to be covered.
    :param neighbourhood_scale: percentage of sets in tentative solution to be removed at each iteration; magnitude of neighbourhood-search
    :param search_depth: percentage of set cost(=length) that is accepted for new solution at each iteration; control for search-depth
    :param solution: a feasible solution to start with
    :param print_logs: prints outputs and parameters of used functions.
    :return: solution set containing a sub-collection of indices of set_collection
    """

    if print_logs:
        print("\n")
        print("| Local-Search-Heuristic |")
        print()



    """
    Initialization & Pre-processes
    """

    feasible_solution = solution
    amount_elements_covered_dict = amount_elements_covered_dict


    set_collection = deepcopy(sets)


    # 0.
    if print_logs:
        print("Initialization.")

    removed_from_solution = list()

    current_solution_list_indices = list(feasible_solution)

    set_lengths = compute_set_lengths(get_set_list_of_solution_indices(collection=sets, solution_indices=current_solution_list_indices))
    d = 0
    D = neighbourhood_scale * len(current_solution_list_indices)
    maximum_set_length_allowed = max(set_lengths) * search_depth



    """
    Main Algorithm
    """
    if print_logs:
        print("\nMain Algorithm.")
        print("Solution optimization by simulated annealing approach")
        print("Removing sets from solution randomly...")

    while d <= D:
        # 1. Randomly select a set from solution
        current_set_index = random.choice(current_solution_list_indices)

        # 2. Move the set from solution to not-covered;
        removed_from_solution.append(current_set_index)
        current_solution_list_indices.remove(current_set_index)

        for element in set_collection[current_set_index]:
            amount_elements_covered_dict[element] -= 1

        d += 1

    if print_logs:
        print("\nCheck which elements now got uncovered...")
        print("Checking which sets are short enough to be brought into solution again")
        print("and how many elements get 'recovered' by those sets...\n")
        print("---Amount Elements uncovered now: ", len(amount_elements_covered_dict), "\n")

    uncovered_elements_existing = True
    # If all elements are still covered, go to step 6, otherwise continue with step 4.
    while uncovered_elements_existing: # should be True if that dict has entries!
        # 3. Update the dict: set the elements that are still covered (-> value is higher than 0)
        uncovered_count = 0
        for element in amount_elements_covered_dict:
            if amount_elements_covered_dict[element] == 0:
                uncovered_count += 1

        if print_logs:
            print("Uncovered Words: ", uncovered_count)

        if (len(elements)-uncovered_count)/len(elements) > 0.9:
            break
        if uncovered_count == 0:
            break



        # 4. Make a dict of sets which have a length that lower-equals maximum_set_length_allowed
        # and recover enough uncovered elements
        recovering_dict = defaultdict()
        for set_i in removed_from_solution:

            # Checking set size
            set_length = len(set_collection[set_i])
            if set_length <= maximum_set_length_allowed:

                # Initialize set value with 0
                recovering_dict[set_i] = 0

                # Compute how many current-uncovered-elements this set recovers and save it as value in recovering_dict
                for element in amount_elements_covered_dict:
                    if amount_elements_covered_dict[element] != 0:
                        continue
                    if element in set_collection[set_i]:
                        recovering_dict[set_i] += 1

                if recovering_dict[set_i] == 0:
                    del recovering_dict[set_i]


                else:  # Taking the amount recovering sets worked best
                    recovering_dict[set_i] = set_length / recovering_dict[set_i]  # Quite slow!
                    # recovering_dict[set_i] = recovering_dict[set_i] / set_length    # Totally bad!!


        # Select a set where the "cost"-value of the recovering_dict is minimum
        key_of_cost_min = min(recovering_dict.keys(), key=(lambda k: recovering_dict[k]))
        key_of_cost_max = max(recovering_dict.keys(), key=(lambda k: recovering_dict[k]))

        current_solution_list_indices.append(key_of_cost_min)
        removed_from_solution.remove(key_of_cost_min)

        if print_logs:
            print("\nSet moving from not-in-solution to in-solution: ", key_of_cost_min,
                  "Amount of sets in current solution: ", len(current_solution_list_indices))

        for element in set_collection[key_of_cost_min]:
            amount_elements_covered_dict[element] += 1

    # 6. Remove all duplicates
    solution_indices = set(current_solution_list_indices)


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

    bla = random.sample(sets_universe, 1)
    print(bla)
    print(bla.__class__)
    print(sets_universe.__class__)
