from collections import defaultdict
from math import log

from text_coverage_data import wds_universe, sets_universe


# Greedy / GA

# Greedy Heuristic
def disk_friendly_greedy(elements, set_collection, p, print_logs=False):
    """
    An special implementation of the greedy algorithm to cover large data sets. It is based on building
    sub-collections by the size of the sets given which might be faster for modern data sizes.

    This approach is the main contribution of:
        Cormode, G., Karloff, H., & Wirth, A. (n.d.). Set Cover Algorithms For Very Large Datasets.
        http://dimacs.rutgers.edu/~graham/pubs/papers/ckw.pdf

    :param elements: universe of len_elements items to be covered; = wds_universe   (1)
    :param set_collection: collection of len_set_collection subsets; = sets_universe (2)
    :param p: parameter > 1; rules the sizes of the created sub-collections. approximation and running time factor (3)
    :param print_logs: prints outputs and parameters of used functions.
    :return: solution list containing a sub-collection of indices of set_collection
    """

    # List of important variables, constants and lists:
    #
    # elements          (1)     <class 'set'>                    { 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I' }
    # set_collection    (2)     <class 'list'> containing 'set's [{'C', 'B', 'A'}, {'G', 'H'}, {'H', 'E'}, {'I'}, {'E'}]
    # p                 (3)     float
    #
    # solution_indices  (4)     <class 'set'>                    { 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I' }
    # covered_elements  (5)     <class 'set'>                    { 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I' }
    #
    # inverted_index    (6)     defaultdict(<class 'list'>, {'F': [1, 2], 'G': [1, 2, 3, 4], 'H': [4, 5], 'I': [6, 9]})
    # set_lengths       (7)     <class 'list'>  containing same i's as (2)      [5, 5, 3, 3, 2, 2, 2, 1, 1, 1]
    # subcollections    (8)     <class 'list'>  containing set's [{8, 9, 7}, {2, 3, 4, 5, 6}, {0, 1}]
    #
    # k and K           (9a,9b) int's

    # Saving the amount of the elements to be covered and the collection size.
    # For the final experiment using the reuters corpus from nltk these values are:
    # |elements|        = len_elements = 29.181;
    # |set_collection|  = len_set_collection = 54.716
    # len_elements = len(elements)
    # len_set_collection = len(set_collection)

    print("+----------------------+")
    print("| Disk-Friendly Greedy |")
    print("+----------------------+\n")

    """
    Pre-processes
    """


    # Lists for saving the solution-subcollection and the so-far-covered elements ((to know, when we can stop.)) ! Is this even checked?! No!
    # In the end we have
    # (4) the indices of sets in set_collection, which made it to be part of the solution and
    # (5) all covered elements, which must be the same as elements-list. ((If those 2 lists contain the
    #     same elements, algorithm is finished.)) TODO Same here!
    solution_indices = set()   # (4)
    covered_elements = set()   # (5)



    # Create an inverted index (6) from our set_collection
    # and save it as defaultdict(<class 'list'>, ...)
    inverted_index = build_inverted_index(set_collection, print_output=print_logs)  # (6)


    # Compute lengths for each set and save it in list. We then get a list of lengths of sets (7)
    # set_length[i] corresponds to same set as set_collection[i]
    set_lengths = compute_set_lengths(set_collection)    # (7)


    # Build sub-collections as list of lists (8) for efficient partitioning of the given set_collection.
    # The sub-collections are partitioned by the lengths of the sets as following:
    #           p^k-1  <=  set_length[i]  <  p^k    ; with
    # p as a approximating factor greater 1;
    # and  k (9a) as an iterating number;
    # Sk := set_length[i];
    # K (9b) may be the greatest k with non-empty Sk.
    # This approach is the main contribution of Cormode et al.
    subcollections, K = build_subcollections(p, set_collection,  set_lengths,                   # (8),(9b)
                                             print_params=print_logs, print_output=print_logs)



    """
    Main Algorithm
    """

    print(subcollections)
    print("\n")

    # 1. Loop in the algorithm.
    # Iterating from subcollection with the longest sets down
    # to the subcollection with set_lengths higher than 1.
    k = K
    while k > 1:
        print("k: ", str(k))
        pk_lower = pow(p, k-1)
        pk_higher = pow(p, k)

        # For each subcollection in subcollections (iterating backwards from highest index to lowest)
        i = len(subcollections)-1
        while i >= 0:
            for set_i in subcollections[i]:
                # { Si \ C };
                # if there are already covered elements in set_collection[set_i]:
                # - remove them from the set,
                # - update the inverted index by removing the index,
                # - add it to the next subcollection Sk-1
                for element in covered_elements:
                    elements_occurances = inverted_index.get(element)
                    if set_i in elements_occurances:
                        set_collection[set_i].remove(element)
                        inverted_index[element] = elements_occurances.remove(set_i)
                        # subcollections[i].remove(set_i)
                        subcollections[i - 1].append(set_i)

                # | Si \ C | >= p^(k-1) ;
                # if the set is still longer than p^(k-1) after covered-elements-removal from set:
                # add index of set_collection[set_i] (=> set_i ) to solution_indices
                if len(set_collection[set_i]) >= pk_lower:
                    solution_indices.add(set_i)
                    print(len(set_collection[set_i])) # <- one set
                    print("***\n")

                # if the set length after covered-elements-removal is below the bound p^(k-1) then
                #
                else:
                    print()
            i -= 1
        k -= 1
    print("k: after all ", str(k))

    # 2. Loop in the algorithm.
    # The last remaining subcollection is that one that only contains sets with set_length = 1.
    for set_i in subcollections[0]:
        for element in covered_elements:
            elements_occurances = inverted_index.get(element)
            if set_i in elements_occurances:
                set_collection[set_i].remove(element)
                inverted_index[element] = elements_occurances.remove(set_i)
                subcollections[i - 1].append(set_i)
            else:
                solution_indices.add(set_i)


    return solution_indices



def build_inverted_index(set_collection, print_output=False):
    """
    Builds an inverted index from a collection of sets.
    :param set_collection: collection of sets
    :param print_output: if set true, the index is printed out
    :return: the inverted index as defaultdict containing lists

    Example:

    defaultdict(<class 'list'>,
        {'A': [0, 1, 2, 7], 'B': [0, 1, 3], 'D': [0, 1],
         'C': [0, 3, 6],    'E': [0, 5, 8], 'G': [1, 2, 3, 4],
         'F': [1, 2],       'H': [4, 5],    'I': [6, 9]})

    """
    print("Building an Inverted Index of given sets...")
    index = defaultdict(list)
    for i in range(len(set_collection)):
        for word in set_collection[i]:
            index[word].append(i)

    if print_output:
        print("Inverted Index defaultdict:")
        print(index)
        print()
        print("Length of index(= len(elements): ", str(len(index)))
        print()
        print("Keys:")
        print(index.keys())
        print()
        print("Items:")
        print(index.items())
        print("---------------------------------\n")

    return index


def compute_set_lengths(set_collection):
    """
    Compute lengths for each set in set_collection and save it in an list.
    :param set_collection: the collection of sets
    :return: list containing the corresponding lengths; indices are the same as in set_collection
    """
    print("Compute lengths of the sets...")
    set_lengths = list()
    for i in range(len(set_collection)):
        set_lengths.append(len(set_collection[i]))
    return set_lengths


def build_subcollections(p, set_collection, set_lengths, print_params=False, print_output=False):
    """
    Seperate sets in Sk subcollections; k is lowest exponent on p, K is the highest
    :param p: rules the sizes of the created sub-collections. see also documentation in disk_friendly_greedy()
    :param set_collection: collection of sets
    :param set_lengths: list containing the lengths of the set in the whole set_collection; indices are the same
    :param print_params: if set true, parameters p, k, K and p^K are printed out
    :param print_output: if set true, the subcollections are printed out
    :return subcollections: the subcollections as list of set's
    :return K: highest k calculated - needed as higher bound in disk_friendly_greedy()
    """
    if print_params or print_output:
        print("---------------------------------\n")

    print("Building subcollections of given sets...")

    subcollections = []
    k = 1
    K = log(max(set_lengths), p)
    while k < K + 1:
        subcollections.append(set())
        for i in range(len(set_lengths)):
            if pow(p, k - 1) <= set_lengths[i] & set_lengths[i] < pow(p, k):
                subcollections[k - 1].add(i)
        k += 1

    if print_params:
        print("Parameters:")
        print("max(set_lengths): ", str(max(set_lengths)))
        print("p: ", str(p))
        print("K: ", str(K))
        print("p^K: ", str(pow(p, K)))
        print("")
        print("K+1: ", str(K + 1))
        print("k: ", str(k), "  # After subcollectioning - also is the 'new' K")
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

    K = k
    return subcollections, K



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

    # solution = disk_friendly_greedy(wds_universe, sets_universe, p=2, print_logs=TRUE)
    solution = disk_friendly_greedy(wds_2, test_sets_2, p=2, print_logs=False)
    print("\n+++++++")
    print("Solution:")
    print(solution)
