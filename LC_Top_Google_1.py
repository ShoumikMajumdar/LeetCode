from re import L
from modules import TreeNode


def reversePolishNotation(tokens):
    """
    https://leetcode.com/problems/evaluate-reverse-polish-notation/
    Evaluate the value of an arithmetic expression in Reverse Polish Notation.
    Valid operators are +, -, *, and /.
    Each operand may be an integer or another expression.

    Space: O(n)
    Time: O(n)
    """

    def math(op1, op2, opn):
        op1 = int(op1)
        op2 = int(op2)

        if opn == "+":
            return op1 + op2

        elif opn == "-":
            return op1 - op2

        elif opn == "*":
            return op1 * op2

        else:
            return int(op1 / op2)

    stack = []
    operators = set(["+", "-", "*", "/"])

    for token in tokens:
        if token not in operators:
            stack.append(token)

        elif token in operators:
            op2 = stack.pop()
            op1 = stack.pop()
            res = math(op1, op2, token)
            stack.append(res)

    # print(stack)
    return stack.pop()


def MeetingRoom2(intervals):
    """
    https://leetcode.com/problems/meeting-rooms-ii/
    Given an array of meeting time intervals where intervals[i] = [starti, endi],
    return the minimum number of conference rooms required.
    """

    if not intervals:
        return 0

    res = 0

    start_times = sorted(i[0] for i in intervals)
    end_times = sorted(i[1] for i in intervals)

    start = 0
    end = 0

    while start < len(intervals):
        # No room avail, need a new room
        if start_times[start] < end_times[end]:
            res += 1

        # Room avail
        else:
            end += 1

        start += 1

    return res


def CombinationSum(candidates, target):
    """
    Given an array of distinct integers candidates and a target integer target,
    return a list of all unique combinations of candidates where the chosen numbers sum to target.
    You may return the combinations in any order.

    The same number may be chosen from candidates an unlimited number of times. Two combinations are unique if
    the frequency of at least one of the chosen numbers is different.
    """

    def helper(candidates, target, path, ret):

        if target < 0:
            return

        if target == 0:
            print(f"Found target with path {path}")
            ret.append(path)
            return

        for i in range(len(candidates)):
            helper(
                candidates[i + 1 :], target - candidates[i], path + [candidates[i]], ret
            )

    ret = []
    path = []
    helper(candidates, target, path, ret)
    return ret


def subsets(nums):
    """
    Given an integer array nums of unique elements, return all possible subsets (the power set).
    The solution set must not contain duplicate subsets. Return the solution in any order.
    """

    def helper(nums, path, res):
        res.append(path)
        for i in range(len(nums)):
            helper(nums[i + 1 :], path + [nums[i]], res)

    res = []
    helper(nums, [], res)
    return res


def main():
    # tokens = ["2", "1", "+", "3", "*"]
    # print(f"Reverse Polish Notation: {reversePolishNotation(tokens)}")

    # intervals = [[1, 10], [2, 7], [3, 19], [8, 12], [10, 20], [11, 30]]
    # print(f"Meeting rooms 2: {MeetingRoom2(intervals)}")

    candidates = [2, 5, 2, 1, 2]
    # print(f"Combination sum:", CombinationSum(candidates, 5))

    # print(f"Subsets: {subsets(candidates)}")


if __name__ == "__main__":
    main()
