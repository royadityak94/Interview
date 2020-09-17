from typing import List

def delete_all(lst: List[int], i: int) -> None:
    # [TODO]: implement this function
    idx = 0
    while idx < (len(lst)):
        # Time Complexity: O(N), Space Complexity: O(1)
        if lst[idx] == i:
            del lst[idx]
        else:
            idx +=1
    return

## an example test

def test_1():
    l = [2, 3, 4, 1, 1, 8, 6, 7]
    i = 1
    delete_all(l, i)
    try:
        assert all(x != i for x in l)
        print ("First use case passed successfully.")
    except AssertionError:
        print ("First use case failed.")

def test_2():
    l = [2, 7, 3, 4, 1, 7, 1, 8, 6, 7, 7]
    i = 7
    delete_all(l, i)
    try:
        assert all(x != i for x in l)
        print ("Second use case passed successfully.")
    except AssertionError:
        print ("Second use case failed.")

def test_3():
    l = [2, 2, 2, 2, 7, 3, 4, 1, 2, 2, 7, 1, 8, 6, 7, 7, 2, 2, 2]
    i = 7
    delete_all(l, i)
    try:
        assert all(x != i for x in l)
        print ("Third use case passed successfully.")
    except AssertionError:
        print ("Third use case failed.")

def test():
    test_1()
    test_2()
    test_3()

test()

l = [10996, 7, 3, 12879, -529, 19634, 14085, -696, 4992, 3, 15833, 3, 18687, 18616, 3, 1294, 17015, 5644, 5974, 9771, 3654, 3, 5002, 17847, 3, 19028, 9894, -975, 3, 3272, 3, 11270, 3, 5206, 8768, 4570, 3, 6860, 3, 14281, 18479, 13325, 7769, 3, -949, 3, 15650, 4498, 3, 5605, 10545, 16687, 13367, 19704, 10495, 3, 3, 10783, 3, 3, -575, 13831, 6628, 14608, 5772, 14868, 10115, 3, 11267, 2543, 5251, -212, 19595, 12803, 1569, 5975, -882, 4417, 15920, 5539, 17797, 7981, 18496, 10258, 17235, 189, 19962, 1597, -197, 15413, 7995, 3006, 17939, 19926, 18144, 3, 6230, 16192, 15041, 5878, 6270, 17387, 14307, 4939, 3771, 8167, 12254, 3, 12826, 18460, 3, 3, 12671, 11922, 420, 10763, 929, 11985, 3155, 1882, 8122, 19722, 8649, 13171, 11118, 6947, 2610, 3992, 3, 14421, 3, 2003, 1111, 11633, 2551, 10974, 3, 9537, 10212, 4021, 6763, 14348, -992, 3, 19467, 10685, 5527, 4697, 17060, 3, 9107, 2433, 3, 19667, 19919, 5754, 7771, 10260, 7724, 3, 3, 3, 12783, 3, 6296, 377, 5966, -697, 12401, 17974, -904, 7736, 16102, 18848, 3, 10505, 17050, 5226, 3, 5003, 18287, 15788, 19387, 3, 3, 3, 10092, 11616, 16944, 13088, 12298, 1171, 3, 18947, 3, 1606, 8670, 3, -298, 8711]
print (len(l))
delete_all(l, 3)
print(len(l))
