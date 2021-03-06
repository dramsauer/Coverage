import math
from copy import deepcopy
from math import log

from src.preprocesses import *
from text_coverage_data import sets_universe

from collections import *


def disk_friendly_greedy(sets, p, max_subcol_size=3000, print_logs=False):
    """
    An special implementation of the greedy algorithm to cover large data sets. It is based on building
    sub-collections by the size of the sets given which might be faster for modern data sizes.

    This approach is the main contribution of:
        Cormode, G., Karloff, H., & Wirth, A. (n.d.). Set Cover Algorithms For Very Large Datasets.
        http://dimacs.rutgers.edu/~graham/pubs/papers/ckw.pdf

    :param sets: / set_collection: collection of len_set_collection subsets / and a copy of it; = sets_universe (1)
    :param p: parameter > 1; rules the sizes of the created sub-collections. approximation and running time factor (2)
    :param max_subcol_size: maximum size of a sub-collection

    :param print_logs: prints outputs and parameters of used functions.
    :return: solution list containing a sub-collection of indices of set_collection
    """

    # List of important variables, constants and lists:
    #
    # set_collection    (1)     <class 'list'> containing 'set's
    # p                 (2)     float

    # solution_indices  (3)     <class 'set'>
    # covered_elements  (4)     <class 'set'>
    #
    # inverted_index    (5)     defaultdict(<class 'list'>) Example: {'F': [1, 2], 'G': [1, 2, 3, 4], 'H': [4, 5], 'I': [6, 9]}
    # set_lengths       (6)     <class 'list'>  containing same indices i as in (2)
    # subcollections    (7)     <class 'list'>  containing set's Example: [{8, 9, 7}, {2, 3, 4, 5, 6}, {0, 1}]
    #
    # k and K           (8a,8b) int's

    print("+----------------------+")
    print("| Disk-Friendly Greedy |")
    print("+----------------------+\n")

    set_collection = deepcopy(sets) # (1)
    print("Selected p-Value: ", p)  # (2)
    print("Number of sets for covering: ", str(len(set_collection)), "\n")



    """
    Initialization & Pre-processes
    """
    print("Initialization.")


    # Lists for saving the solution-subcollection and the so-far-covered elements
    # In the end we have
    # (3) the indices of sets in set_collection, which made it to be part of the solution and
    # (4) all covered elements
    solution_indices = set()   # (3)
    covered_elements = set()   # (4)



    # Create an inverted index (5) from our set_collection
    # and save it as defaultdict(<class 'list'>, ...)
    inverted_index = build_inverted_index(set_collection, print_output=print_logs)  # (5)


    # Compute lengths for each set and save it in list. We then get a list of lengths of sets (6)
    # set_length[i] corresponds to same set as set_collection[i]
    set_lengths = compute_set_lengths(set_collection)    # (6)


    # Build sub-collections as defaultdict of lists (7) for efficient partitioning of the given set_collection.
    # The sub-collections are partitioned by the lengths of the sets as following:
    #           p^k-1  <=  set_length[i]  <  p^k    ; with
    # p as a approximating factor greater 1;
    # and  k (8a) as an iterating number (saved as keys in the dict);
    # Sk := set_length[i];
    # K (8b) may be the greatest k with non-empty Sk.
    # This approach is the main contribution of Cormode et al.
    subcollections = build_subcollections(p, set_collection,  set_lengths, max_subcol_size=max_subcol_size, print_params=print_logs, print_output=print_logs) # (7)
    k_values = subcollections.keys()    # (8)
    k = max(k_values)                   # = (8b)


    """
    Main Algorithm
    """

    # 1. Loop in the algorithm.
    # Iterating from subcollection with the longest sets down
    # to the subcollection with set_lengths higher than 1.
    print("\nFirst loop.")
    while k > 1:
        pk_lower = pow(p, k-1)
        try:
            for set_i in subcollections.get(k):

                # | Si \ C | >= p^(k-1) ;
                if set_lengths[set_i] >= pk_lower:
                        # if there are already elements covered which are in set_collection[set_i]:
                        # - update the inverted index by removing the index, (a)
                        # - remove them from the set, (b)
                        # - add it to the subcollection Sk' where p^k-1 <= set_length[set_i] < p^k, (c)
                        if len(covered_elements) > 0:
                            for element in covered_elements:
                                # { Si(element) € C }:
                                if element not in set_collection[set_i]:
                                    continue
                                # { Si(element) \ C }:
                                else:
                                    elements_occurrences = inverted_index.get(element)
                                    if set_i in elements_occurrences:
                                        elements_occurrences.remove(set_i)              # (a)
                                        inverted_index[element] = elements_occurrences  # (a)

                                        set_collection[set_i].remove(element)           # (b)
                                        set_lengths[set_i] -= 1

                            if set_lengths[set_i] >= pk_lower:
                                current_col = subcollections.get(k)
                                current_col.remove(set_i)
                                if set_lengths[set_i] != 0:
                                    new_k = int(math.ceil(log(set_lengths[set_i], p)))+1
                                    # b = pow(p, new_k - 1) <= set_lengths[set_i] & set_lengths[set_i] < pow(p, new_k)
                                    try:
                                        next_col = subcollections.get(new_k)
                                        next_col.append(set_i)
                                        subcollections[k-1] = next_col  # (c)
                                    except AttributeError:
                                        pass
                                continue

                        solution_indices.add(set_i)
                        for element in set_collection[set_i]:
                            if element not in covered_elements:
                                covered_elements.add(element)
                            elements_occurrences = inverted_index.get(element)
                            if set_i in elements_occurrences:
                                elements_occurrences.remove(set_i)
                                inverted_index[element] = elements_occurrences
        except TypeError:
            pass
        k -= 1


    if print_logs:
        print("Already covered after 1. loop: ", covered_elements)
        print("# Already covered after 1. loop: ", len(covered_elements))

    # 2. Loop in the algorithm.
    # The last remaining subcollection is that one that only contains sets with set_length = 1.
    print("\nSecond loop.")
    try:
        for set_i in subcollections.get(1):
            for element in covered_elements:
                if set_lengths[set_i] == 1:
                    if set_collection[set_i].pop() not in covered_elements:
                        solution_indices.add(set_i)
                        covered_elements.add(element)
                    set_lengths[set_i] -= 1
    except TypeError:
        pass
    return solution_indices


def is_set_length_higher_or_equal_pk_lower(pk_lower, set_i, set_lengths):
    set_length_bigger_pk_lower = set_lengths[set_i] >= pk_lower
    return set_length_bigger_pk_lower


def build_subcollections(p, set_collection, set_lengths, max_subcol_size=3000, print_params=False, print_output=False):
    """
    Seperate sets in Sk subcollections; k is lowest exponent on p, K is the highest
    :param max_subcol_size: maximum size of a sub-collection
    :param p: rules the sizes of the created sub-collections. see also documentation in disk_friendly_greedy()
    :param set_collection: collection of sets
    :param set_lengths: list containing the lengths of the set in the whole set_collection; indices are the same
    :param print_params: if set true, parameters p, k, K and p^K are printed out
    :param print_output: if set true, the subcollections are printed out
    :return subcollections: the subcollections as defaultdict of lists
    """
    if print_params or print_output:
        print("---------------------------------\n")

    print("Building subcollections of given sets and index them in a dict...")

    subcollections = defaultdict(list)

    K = log(max(set_lengths), p)
    for k in range(1, math.ceil(K)+1):
        for i in range(len(set_lengths)):
            if round(pow(p, k - 1)) <= set_lengths[i] & set_lengths[i] < round(pow(p, k)):
                subcollections[k].append(i)
            if len(subcollections[k]) > max_subcol_size:
                break

    if print_params:
        print("Parameters:")
        print("max(set_lengths): ", str(max(set_lengths)))
        print("p: ", str(p))
        print("K: ", str(K))
        print("p^K: ", str(pow(p, K)))
        print("")
        print("K+1: ", str(K + 1))
        print("k: ", str(k), "  # After subcollectioning - also is the 'new' K")
        print("p^K: ", str(pow(p, K)), "  # After subcollectioning")
        print("p^K+1: ", str(pow(p, K+1)), "  # After subcollectioning")
    if print_output:
        print("\n---   ---   ---   ---   ---   ---")
        print("Subcollections:")
        print(subcollections)
        for i in range(len(subcollections)):
            print("Subcollection #", str(i), ":")
            for j in range(len(subcollections[i])):
                set_num = subcollections[i][j]
                print(set_collection[set_num])
        print("---------------------------------\n")

    return subcollections



if __name__ == "__main__":
    print("")

    """
    Execution of the disk-friendly greedy algorithm for the given set cover problem.
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

    solution = disk_friendly_greedy(wds_2, test_sets_2, p=2, print_logs=False)
    print("\n+++++++")
    print("Solution:")
    print(solution)
