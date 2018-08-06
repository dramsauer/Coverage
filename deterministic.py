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


if __name__ == "__main__":
    print("Start Greedy:")
    # solution = greedy(wds_universe, sets_universe)
    # print(solution)
