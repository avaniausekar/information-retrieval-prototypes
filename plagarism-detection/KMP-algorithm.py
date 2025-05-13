# Knuth–Morris–Pratt algorithm
# Efficient search algo
# LPS = longest prefix suffix portion
# lps array = size of pattern
# Awesome algorithm - mind blownnnnn
# O(m + n)

# we want to find a needle(substring) into haystack (string)

def KMP(haystack, needle):
    if needle == "":
        return 0

    lps = [0] * len(needle)
    prevLps, i = 0, 1
    while i < len(needle):
        if needle[i] == needle[prevLps]:
            lps[i] = prevLps + 1
            prevLps += 1
            i += 1
        elif prevLps == 0:
            lps[i] = 0
            i += 1
        else:
            prevLps = lps[prevLps - 1]
            i += 1

    
    i = 0 # pts for haystack
    j = 0 # ptr for needle
    while i < len(haystack):
        if haystack[i] == needle[j]:
            i += 1
            j += 1
        else:
            if j == 0:
                i += 1
            else:
                j = lps[j-1]
        
        if j == len(needle):
            return i - len(needle)
    
    # if no match found
    return -1

# index = KMP("AAAXAAAX","AAAA") -1

index = KMP("AAAXAAAA","AAAA")
if index == -1:
    print("No matches were found")
else:
    print("First occurance is at ",index)