# Also called deletion distance/levenshtein distance
import unittest

def calculate_levenshtein_distance(str1, str2):
    if not str1 and not str2:
        return 0
    if not str1 and str2:
        return len(str2)
    if str1 and not str2:
        return len(str1)
    else:
        return calculate_levenshtein_distance_recursive(str1, str2, len(str1), len(str2))

def calculate_levenshtein_distance_recursive(str1, str2, i, j):
    # Time Complexity = Space Complexity: O(2^(max(len(str1), len(str2))))
    if i == 0:
        return j
    if j == 0:
        return i

    if str1[i-1] == str2[j-1]:
        return calculate_levenshtein_distance_recursive(str1, str2, i-1, j-1)
    else:
        return 1 + min(calculate_levenshtein_distance_recursive(str1, str2, i-1, j),
            calculate_levenshtein_distance_recursive(str1, str2, i, j-1))

def calculate_levenshtein_distance_dp(str1, str2):
    # Time Complexity = Space Complexity: O(MN)
    if not str1 and not str2:
        return 0
    if not str1 and str2:
        return len(str2)
    if str1 and not str2:
        return len(str1)

    dp = [[-1 for _ in range(len(str2)+1)] for _ in range(len(str1)+1)]

    # Filling column 0
    for row in range(len(str1)+1):
        dp[row][0] = row
    # Filling row 0
    for col in range(len(str2)+1):
        dp[0][col] = col

    # Populating across all other subsets
    for i in range(1, len(str1)+1):
        for j in range(1, len(str2)+1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1])

    return dp[len(str1)][len(str2)]

class Test(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_recursion(self):
        # Using plain recursion
        self.assertEqual(calculate_levenshtein_distance("dog", "frog"), 3)
        self.assertEqual(calculate_levenshtein_distance("some", "some"), 0)
        self.assertEqual(calculate_levenshtein_distance("some", "thing"), 9)
        self.assertEqual(calculate_levenshtein_distance("", ""), 0)
        self.assertEqual(calculate_levenshtein_distance("", "blue"), 4)
        self.assertEqual(calculate_levenshtein_distance("blue", ""), 4)

    def test_dp(self):
        # Using Dynamic Programming
        self.assertEqual(calculate_levenshtein_distance_dp("dog", "frog"), 3)
        self.assertEqual(calculate_levenshtein_distance_dp("some", "some"), 0)
        self.assertEqual(calculate_levenshtein_distance_dp("some", "thing"), 9)
        self.assertEqual(calculate_levenshtein_distance_dp("", ""), 0)
        self.assertEqual(calculate_levenshtein_distance_dp("", "blue"), 4)
        self.assertEqual(calculate_levenshtein_distance_dp("blue", ""), 4)

def main():
    unittest.main()

main()
