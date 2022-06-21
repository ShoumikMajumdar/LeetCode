def subsets(nums):
    """
    Given an integer array nums of unique elements, return all possible subsets (the power set).
    The solution set must not contain duplicate subsets. Return the solution in any order.

    https://leetcode.com/problems/subsets/
    """

    def helper(nums, path, res):
        res.append(path)
        for i in range(len(nums)):
            helper(nums[i + 1 :], path + [nums[i]], res)

    res = []
    helper(nums, [], res)
    return res


def CombinationSum(candidates, target):
    """
    Given an array of distinct integers candidates and a target integer target,
    return a list of all unique combinations of candidates where the chosen numbers sum to target.
    You may return the combinations in any order.

    The same number may be chosen from candidates an unlimited number of times. Two combinations are unique if
    the frequency of at least one of the chosen numbers is different.


    https://leetcode.com/problems/combination-sum/
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


def CombinationSum2(candidates, target):
    """
    Given a collection of candidate numbers (candidates) and a target number (target),
    find all unique combinations in candidates where the candidate numbers sum to target.
    Each number in candidates may only be used once in the combination.
    Note: The solution set must not contain duplicate combinations.

    https://leetcode.com/problems/combination-sum-ii/
    """

    def helper(idx, candidates, target, path, res):
        if target < 0:
            return

        if target == 0:
            res.append(path)
            return

        for i in range(idx, len(candidates)):
            if i > idx and candidates[i] == candidates[i - 1]:
                continue
            helper(
                i + 1, candidates, target - candidates[i], path + [candidates[i]], res
            )

    candidates.sort()
    res = []
    helper(0, candidates, target, [], res)
    return res


def main():
    candidates = [2, 5, 2, 1, 2]
    # print(f"Subsets: {subsets(candidates)}")
    # print(f"Combination sum:", CombinationSum(candidates, 5))
    print(f"Combination sum:", CombinationSum2(candidates, 5))


if __name__ == "__main__":
    main()
