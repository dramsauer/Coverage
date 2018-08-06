import re
from collections import defaultdict, Counter

from text_coverage_data import wds_universe, sets_universe


# Greedy / GA

# Greedy Heuristic
def greedy(X, S):
    """
    :param X: universe of n items; = wds_universe
    :param S: collection of m subsets; sets_universe
    :return: solution list containing a sub-collection of indices of S
    """

    # |X| = n = 29.181; |S| = m = 54.716
    n = len(X)
    m = len(S)

    # E := set of indices of sets in the solution; C := elements covered so far
    E = list()
    C = list()

    # TODO add inverted index here

    while len(C) != n:
        print("*******************")
        # print(len(C))
        # print(n)
        # print(m)
        # C.append(1)
    return E


def index_sets(sets):
    index = defaultdict(list)

    # for id, set in enumerate(sets):
    #    for word in set:
    #        index[word].append(id)

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

    # solution = greedy(wds_universe, sets_universe)
    # print(solution)
