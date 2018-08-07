from collections import defaultdict

from text_coverage_data import wds_universe, sets_universe


# Greedy / GA

# Greedy Heuristic
def disk_friendly_greedy(elements, set_collection, p):
    """
    :param elements: universe of len_elements items to be covered; = wds_universe
    :param set_collection: collection of len_set_collection subsets; = sets_universe
    :param p: parameter > 1; rules the sizes of the created sub-collections. approximation and running time factor
    :return: solution list containing a sub-collection of indices of set_collection
    """

    # |elements| = len_elements = 29.181; |set_collection| = len_set_collection = 54.716
    len_elements = len(elements)
    len_set_collection = len(set_collection)

    # solution_indices := set of indices of sets in the solution; covered_items := elements covered so far
    solution_indices = list()
    covered_items = list()

    # Create an inverted index
    # inverted_index = index_sets()

    # Compute length for each set and save it in list. set_length[i] corresponds to same set as set_collection[i]
    set_lengths = list()
    for i in range(len_set_collection):
        set_lengths.append(len(set_collection[i]))

    # TODO Algorithm in section 3.2:
    # TODO > Seperate sets in Sk subcollections
    subcollections = list()
    k = 1
    while True:
        for i in range(len(set_lengths)):
            if pow(p, k-1) <= set_lengths[i] & set_lengths[i] < pow(p, k):
                subcollections[k-1] = i
        k += 1
    # TODO >

    # while len(covered_items) != len_elements:
    #    print("*******************")
        # print(len(covered_items))
        # print(len_elements)
        # print(len_set_collection)
        # covered_items.append(1)
    return solution_indices


def index_sets(sets):
    index = defaultdict(list)
    for i in range(len(sets)):
        for word in sets[i]:
            index[word].append(i)
    print("len sets: " + str(len(sets)))

    return index


def index_sets_test(whole_sets_universe=False):
    if not whole_sets_universe:
        test_sets = [sets_universe[0],
                     sets_universe[1],
                     sets_universe[2],
                     sets_universe[3],
                     sets_universe[5],
                     sets_universe[6],
                     sets_universe[7],
                     sets_universe[8],
                     sets_universe[9]
                     ]
    else:
        test_sets = sets_universe

    ind = index_sets(test_sets)

    for item in ind.items():
        print(item)
    print("\n Länge des Indexes: " + str(len(ind)))
    # print(ind.items())
    # print(ind.keys())


if __name__ == "__main__":
    print("")
    # index_sets_test(whole_sets_universe=True)

    solution = disk_friendly_greedy(wds_universe, sets_universe)
    # print(solution)
