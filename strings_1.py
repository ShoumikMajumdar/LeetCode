import math


def isSubsequence(s1, s2):
    """
    Given two strings s1 and s2, if s2 is a subsequence of s1.
    The
        Time: O(n + m)
        Space: O(1)
    """

    s1 = s1.lower()
    s2 = s2.lower()

    if len(s1) == 0 or len(s2) == 0:
        return -1

    if len(s2) > len(s1):
        return False

    pointer = 0
    for i in range(len(s1)):
        print(f"{s2[pointer]} | {s1[i]}")
        if s2[pointer] == s1[i]:
            pointer += 1

    print(pointer)
    if pointer == len(s2):
        return True

    return False


def anagram(s1, s2):
    """
    Given 2 strings, determine if s2 is an anagram of s1.
        Space: O(n)
        Time: O(n+m)
    """

    if len(s1) != len(s2):
        return False

    s1 = s1.lower()
    s2 = s2.lower()

    tab = {}

    for char in s1:
        if char in tab.keys():
            tab[char] += 1
        else:
            tab[char] = 1

    for char in s2:
        if char in tab.keys():
            tab[char] -= 1
        else:
            return False

    vals = tab.values()
    for count in vals:
        if count != 0:
            return False

    return True


def leftmostRepeat(s1):
    """
    Given a string, return the index of the left most character that repeats.
    eg: input = geekgs -> return 0 as g is the left most char that repeats.

    Space: O(n)
    Time: O(n)
    """

    s1 = s1.lower()
    res = math.inf
    tab = {}

    for i in range(len(s1)):
        char = s1[i]
        if char not in tab.keys():
            tab[char] = i
        else:
            if tab[char] < res:
                res = tab[char]

    if res == math.inf:
        return -1

    return res


def reverseWordsInString(s):
    """
    Given a string, reverse the words in the sentance in place.
    eg: I love coding -> coding love I

    Space: O(1)
    Time: O(n)
    """

    def reverse(s, start, end):

        s = list(s)
        while start <= end:
            s[start], s[end] = s[end], s[start]
            start += 1
            end -= 1

        return "".join(s)

    start = 0
    for end in range(len(s)):
        if s[end] == " ":
            s = reverse(s, start, end - 1)
            start = end + 1

    print(end)
    s = reverse(s, start, end)
    s = reverse(s, 0, len(s) - 1)

    return s


def NaivePatternSearching(text, pattern):
    """
    Given a string and a pattern, find index of all occurence of pattern in the string.
    Space: O(1)
    Time : O((n-m+1)*m) -> Quadratic time.
    """
    n = len(text)
    m = len(pattern)
    print(f"Text '{text}' of length {n}")
    print(f"pattern '{pattern}' of length {m}")

    for i in range(n - m + 1):
        for j in range(0, m):
            if text[i + j] != pattern[j]:
                break

        if j == m - 1:
            print(i)


def main():
    s1 = "AAAAA"
    s2 = "AAA"
    # print(f"is Subsequence? : {isSubsequence(s1,s2)}")
    # print(f"is anagram? : {anagram(s1,s2)}")
    # print(f"Left most repeating character {leftmostRepeat(s1)}")
    # print(f"Reverse words in string:  {reverseWordsInString(s1)}")
    # NaivePatternSearching(s1, s2)



if __name__ == "__main__":
    main()
