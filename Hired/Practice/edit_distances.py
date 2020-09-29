import unittest

def calculate_levenshtein_distance(str1, str2):
    if str1 and not str2:
        return len(str1)
    elif not str1 and str2:
        return len(str2)
    elif not str1 and not str2:
        return 0

    return calculate_levenshtein_distance_recursive(str1, str2, len(str1), len(str2))

def calculate_levenshtein_distance_recursive(str1, str2, i, j):
    if i == 0:
        return j
    elif j == 0:
        return i
    else:
        if str1[i-1] == str2[j-1]:
            return calculate_levenshtein_distance_recursive(str1, str2, i-1, j-1)
        else:
            return 1 + min(
                        calculate_levenshtein_distance_recursive(str1, str2, i-1, j),
                        calculate_levenshtein_distance_recursive(str1, str2, i, j-1))

def calculate_levenshtein_distance_td_dp(str1, str2):
    if str1 and not str2:
        return len(str1)
    elif not str1 and str2:
        return len(str2)
    elif not str1 and not str2:
        return 0

    td = [[-1 for j in range(len(str2))] for i in range(len(str1))]
    return calculate_levenshtein_distance_td_dp_recursive(td, str1, str2, len(str1), len(str2))

def calculate_levenshtein_distance_td_dp_recursive(td, str1, str2, i, j):
    if i == 0:
        return j
    elif j == 0:
        return i
    else:
        if td[i-1][j-1] == -1:
            if str1[i-1] == str2[j-1]:
                td[i-1][j-1] = calculate_levenshtein_distance_recursive(str1, str2, i-1, j-1)
            else:
                td[i-1][j-1] = 1 + min(
                            calculate_levenshtein_distance_recursive(str1, str2, i-1, j),
                            calculate_levenshtein_distance_recursive(str1, str2, i, j-1))
        return td[i-1][j-1]

def calculate_levenshtein_distance_dp(str1, str2):
    if str1 and not str2:
        return len(str1)
    elif not str1 and str2:
        return len(str2)
    elif not str1 and not str2:
        return 0

    td = [[-1 for j in range(len(str2)+1)] for i in range(len(str1)+1)]

    # Filling up column - 0, i.e. edit distance = j when i=0
    for j in range(len(str2)+1):
        td[0][j] = j

    # Filling up row - 0, i.e. edit distance = i when j=0
    for i in range(len(str1)+1):
        td[i][0] = i

    # Populating all other subsets
    for i in range(1, len(str1)+1):
        for j in range(1, len(str2)+1):
            if str1[i-1] == str2[j-1]:
                td[i][j] = td[i-1][j-1]
            else:
                td[i][j] = 1 + min(td[i-1][j], td[i][j-1])

    return td[len(str1)][len(str2)]



class Test(unittest.TestCase):
    def setup(self):
        pass
    def teardown(self):
        pass
    def test_recursion(self):
        # Using plain recursion
        self.assertEqual(calculate_levenshtein_distance("dog", "frog"), 3)
        self.assertEqual(calculate_levenshtein_distance("some", "some"), 0)
        self.assertEqual(calculate_levenshtein_distance("some", "thing"), 9)
        self.assertEqual(calculate_levenshtein_distance("", ""), 0)
        self.assertEqual(calculate_levenshtein_distance("", "blue"), 4)
        self.assertEqual(calculate_levenshtein_distance("blue", ""), 4)

    def test_top_down_dp(self):
        # Using top down Dynamic Programming
        self.assertEqual(calculate_levenshtein_distance_td_dp("dog", "frog"), 3)
        self.assertEqual(calculate_levenshtein_distance_td_dp("some", "some"), 0)
        self.assertEqual(calculate_levenshtein_distance_td_dp("some", "thing"), 9)
        self.assertEqual(calculate_levenshtein_distance_td_dp("", ""), 0)
        self.assertEqual(calculate_levenshtein_distance_td_dp("", "blue"), 4)
        self.assertEqual(calculate_levenshtein_distance_td_dp("blue", ""), 4)

    def test_bottom_up_dp(self):
        #Using bottom up Dynamic Programming
        self.assertEqual(calculate_levenshtein_distance_dp("dog", "frog"), 3)
        self.assertEqual(calculate_levenshtein_distance_dp("some", "some"), 0)
        self.assertEqual(calculate_levenshtein_distance_dp("some", "thing"), 9)
        self.assertEqual(calculate_levenshtein_distance_dp("", ""), 0)
        self.assertEqual(calculate_levenshtein_distance_dp("", "blue"), 4)
        self.assertEqual(calculate_levenshtein_distance_dp("blue", ""), 4)

def main():
    unittest.main()

main()
