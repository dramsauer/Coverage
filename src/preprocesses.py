import collections

from text_coverage_data import sets_universe


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
    index = collections.defaultdict(list)
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


def get_set_list_of_solution_indices(collection, solution_indices):
    """
    Getting a list of sets from a list of indices (of a solution)
    :param collection: the sets_universe
    :param solution_indices: iterable containing indices of sets (in a solution) which is represents a sub-collection of collection
    :return: a list containing the corresponding sets
    """

    sets = list()
    for i in solution_indices:
        sets.append(collection[i])
    return sets


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


def sort_collection_by_set_sizes(set_collection):
    """
    Sort a given collection by the size of sets in it by using a dictionary
    :param set_collection: collection of sets
    :return: sorted collection
    """
    set_length_dict = create_set_length_dict(set_collection)

    print("Creating sorted list from dict...")
    sorted_list = list()
    i = min(set_length_dict)
    while i <= max(set_length_dict):
        if set_length_dict.get(i) is not None:
            for set in set_length_dict.get(i):
                sorted_list.append(set_collection[set])
        i += 1
    return sorted_list


def sort_collection_by_set_sizes_with_comparison_list(set_collection):
    """
    Sort a given collection by the size of sets in it by using a dictionary
    :param set_collection: collection of sets
    :return: sorted collection and comparison dict(key: new index of a set, value: original index)
    """
    set_length_dict = create_set_length_dict(set_collection)

    print("Creating sorted list and list for comparing from dict...")
    sorted_list = list()
    comparison_list = list()

    i = min(set_length_dict)
    while i <= max(set_length_dict):
        if set_length_dict.get(i) is not None:
            for set in set_length_dict.get(i):
                sorted_list.append(set_collection[set])
                comparison_list.append(set)
        i += 1

    return sorted_list, comparison_list


def create_set_length_dict(set_collection):
    """
    Builds a dictionary from a collection of sets with the set sizes as keys
    :param set_collection: collection of sets
    :return: the size-dictionary
    """
    print("Building a dictionary of given sets with their lengths as keys:")
    set_length_dict = collections.defaultdict(list)
    lengths = compute_set_lengths(set_collection)
    i = 0
    while i < len(lengths):
        set_length_dict[lengths[i]].append(i)
        i += 1
    return set_length_dict


if __name__ == "__main__":
    sort, comp = sort_collection_by_set_sizes_with_comparison_list(sets_universe)

    print("the:", sets_universe[189])
    print("254 shall be 189:", comp[254])
    print("apr: ", sets_universe[701])
    print("255 shall be 701:", comp[255])
    print("energy: ", sets_universe[731])
    print("256 shall be 731:", comp[256])
    print("reuter: ", sets_universe[1517])
    print("257 shall be 1517:", comp[257])

