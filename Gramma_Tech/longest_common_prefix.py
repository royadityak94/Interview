# This question is asked by Microsoft. Given an array of strings, return the longest common prefix that is shared amongst all strings

def longest_common_prefix(arr):
    common_prefix = arr[0]

    for i in range(1, len(arr)):
        if len(common_prefix) == 0:
            break
        new_string = arr[i]
        for j in range(min(len(common_prefix), len(new_string))):
            if new_string[j] == common_prefix[j]:
                pass
            else:
                common_prefix = new_string[:j]
                break

    return common_prefix



def main():
    print (longest_common_prefix(["colorado", "color", "cold"]))
    print (longest_common_prefix(["a", "b", "c"]))
    print (longest_common_prefix(["spot", "spotty", "spotted"]))
    print (longest_common_prefix(["geeksforgeeks", "geeks", "geek", "geezer"]))

main()
