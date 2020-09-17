# Python program to merge 2 packages

def getIndicesOfItemWeights(arr, limit):
    if not arr:
        return []
    start = (len(arr)//2) - 1
    end = start + 1

    while start >= 0 and end < len(arr):
        current = arr[start] + arr[end]
        if current == limit:
            return [end, start]
        elif current < limit:
            end += 1
        else:
            start -= 1
    return []


# Using Dictionary
def getIndicesOfItemWeights_dict(arr, limit):
    complement = {}
    for idx, num in enumerate(arr):
        if num in complement:
            return sorted([idx, complement[num]], reverse=True)
        else:
            complement[limit-num] = idx

    print (complement)

def get_indices_of_item_wights(arr, limit):
  # Time Complexity: O(N), Space Complexity: O(N)
  if not arr:
    return []
  complement = {}
  for idx, num in enumerate(arr):
    if num in complement:
      return sorted([idx, complement[num]], reverse=True)
    else:
      complement[limit-num] = idx
  return []

def main():
    # print (getIndicesOfItemWeights ([4, 6, 10, 15, 16], 21))
    # print (getIndicesOfItemWeights ([4, 4], 8))
    # print (getIndicesOfItemWeights ([1, 3, 4], 5))
    # print (getIndicesOfItemWeights ([], 5))

    # Dictionary based implementation
    print (getIndicesOfItemWeights_dict ([4, 6, 10, 15, 16], 21))
    # print (getIndicesOfItemWeights_dict ([4, 4], 8))
    # print (getIndicesOfItemWeights_dict ([1, 3, 4], 5))
    # print (getIndicesOfItemWeights_dict ([], 5))



main()
