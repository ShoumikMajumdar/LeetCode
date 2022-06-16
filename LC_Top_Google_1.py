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


def LeavesOfBinaryTree(root):
    pass


def main():
    # tokens = ["2", "1", "+", "3", "*"]
    # print(f"Reverse Polish Notation: {reversePolishNotation(tokens)}")

    # intervals = [[1, 10], [2, 7], [3, 19], [8, 12], [10, 20], [11, 30]]
    # print(f"Meeting rooms 2: {MeetingRoom2(intervals)}")


if __name__ == "__main__":
    main()
