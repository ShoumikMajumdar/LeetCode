import math
from collections import Counter
from collections import defaultdict
from multiprocessing.dummy import Array
def MaxDifference(array):
    """
    Find the max diff between a[i] and a[j] such that j>1

    Naive:
        Space: O(1)
        Time: O(n^2)

    Best:
        Space: O(1)
        Time: O(n)
    """

    if len(array)<2:
        return -1

    # Naive: Nested loop
    # res = -math.inf
    # for i in range(len(array)):
    #     for j in range(i+1, len(array)):
    #         diff = array[j]-array[i]
    #         if diff> res:
    #             res = diff

    # Best: Traverse from left to right. substract each elemet from the min element seen so far. Maintain the MAX difference.
    MIN = array[0]
    res = -math.inf
    for i in range(1,len(array)):
        curr_diff = array[i]-MIN
        res = max(res, curr_diff)
        MIN = min(MIN,array[i])

    return res


def FreqInSortedArray(array):
    """
    Given a sorted Array, find freq of ever element.

    Dict Method:
        Space: O(n)
        Time: O(n)
    
    Print In Place:
        Space: O(1)
        TimeL O(n)
    """
    # Dict method: Traverse through array and keep track of elements and freq in a dict.
    # res = {}
    # for item in array:
    #     if item in res.keys():
    #         res[item]+=1
    #     else:
    #         res[item] = 1

    # Traverse through array and print when element in not equal to previous element. Reset freq to 1.
    freq = 1
    for i in range(1, len(array)):
        if array[i-1] == array[i]:
            freq+=1
        
        else:
            print(f"Element {array[i-1]} | freq {freq}")
            freq = 1
    
    print(f"Element {array[-1]} | freq {freq}") # Printing freq of last element.

def stockBuySellOne(array):
    """
    Max profit that you can make through multiple buys and sells such that you can buy on i and sell on j and j>i
    Complexity:
        Space: O(1)
        Time: O(n)
    """
    # Trverse from left to right starting frm index 1. if a[i]> a[i-1], add profit to total, else continue.
    Max_profit = 0
    for i in range(1,len(array)):
        if array[i]>array[i-1]:
            profit = array[i] - array[i-1] 
            Max_profit+=profit

    return Max_profit

def TrappingRainWater(array):
    """
    Find the max water that can be stored.
    Complexity:
        Space: O(n)
        Time : O(n)
    """
    left = [0]*len(array)
    right = [0]* len(array)

    lmax = array[0]
    left[0] = lmax
    for i in range(1,len(array)):
        lmax = max(lmax,array[i])
        left[i] = lmax
    
    rmax = array[-1]
    right[-1] = rmax
    for i in range(len(array)-2,-1,-1):
        rmax = max(rmax, array[i])
        right[i] = rmax

    total  = 0
    for i in range(1,len(array)-1):
        water = min(left[i],right[i]) - array[i]
        total+=water

    return total

def maxConsecutiveOnes(array):
    """
    Maximum consecutive ones in an array.
    Complexity:
        Space: O(1)
        Time: O(n)
    """

    # Traverse from left to right. Whenever you see a 1, increase frequency and update result. WHen you see a 0, reset freq to 0
    res = 0
    freq = 0
    for i in range(len(array)):
        if array[i]==1:
            freq+=1
            res = max(res, freq)
        else:
            freq = 0
        
        print(f"i: {i}, a[i]:{array[i]}, freq: {freq}, res: {res}")
    
    return res


def MaxSumSubarray(array):
    """
    Given an array, find the max sum of subarray.
    Naive:
        Space: O(1)
        Tine: O(n^2)

    Kadanes:
        Space: O(1)
        Time: O(n)
    """

    # Naive. Run a loop i and loop j = i+1.
    # Init sum as array[i] and res also as array[i] . At each step of loop j, do sum = sum +  array[j]. keep track of res = max(res,sum). res has the max sum of every sub array starting at i and ending at j

    # ans = -math.inf
    # for i in range(len(array)):
    #     sum = array[i]
    #     res = sum
    #     for j in range(i+1,len(array)):
    #         sum+=array[j]
    #         res = max(res,sum)
    #     ans = max(ans,res)
    # return ans

    # Best: Kadanes algorithm. Set running_sum to array[0]. Res = array[0]
    # looping from index 1 to n, running sum is max sum ending at index i. That means, it is max(previous sum + current element, current element). 
    # res keeps track of max sums ending at index i.

    res = array[0]
    sum = array[0]

    for i in range(1,len(array)):
        sum = max(sum + array[i],array[i])
        res = max(res,sum)

    return res

def MaxLengthEvenOdd(array):
    """
    Find max len of subarray where consecutive elemetns are alternative even and odd.
    Complexity:
        Space: O(1)
        Time: O(n)
    """
    res  = 1
    c = 1
    for i in range(1,len(array)):
        if array[i] %2 == 0 and array[i-1]%2!=0:
            c+=1
            res = max(res,c)
        elif array[i]%2!=0 and array[i-1]%2 == 0:
            c+=1
            res = max(res,c)
        else:
            c = 1
    return res

def MaxSumCircular(array):
    """
    Given an array, find the max circular sum of the array. Note that this might just be the max sum in subararray OR the max subarray could be a circular subarray.
    Naive:
        Space: O(1)
        Time: O(n^2)

    Effecient:
        Space: O(1)
        Time: O(n)
    """
    
    #Naive: Loop i from 0 to n. sum = arr[i], res = arr[i]. Loop j from i+1 to n. use modulo arthimatics (i+j)%n to determine next index. Then similar as max sum subarray
    # ans = -math.inf
    # for i in range(len(array)):
    #     sum = array[i]
    #     res = sum 
    #     for j in range(1,len(array)):
    #         index = (i+j)%len(array)
    #         sum = sum + array[index]
    #         res = max(res,sum)
        
    #     ans = max(ans,res)

    # return ans

    # Efficient: Max Circular sum = Max(Max sum of subarray, total_sum of array - min sum of subarray). Note that if max sum of subarray is -ve, return directly.
    
    # Max Sum Kadanes
    Max_sum = array[0]
    sum = array[0]
    for i in range(1,len(array)):
        sum = max(sum + array[i],array[i])
        Max_sum = max(Max_sum,sum)

    print(f"Masx sum of sumarray {Max_sum}")

    # Total sum of array
    total_sum = 0
    for item in array:
        total_sum+=item

    print(f"Total sum of array {total_sum}")

    # Min sum kadanes
    Min_sum = array[0]
    sum = array[0]

    # Min sum kadanes
    for i in range(1,len(array)):
        sum = min(sum+array[i],array[i])
        Min_sum = min(Min_sum,sum)

    print(f"Min sum {Min_sum}")

    # Max circular
    Max_circular_sum = max(Max_sum, total_sum - Min_sum)


    #  if max_sum is negetive, return max_sum. If this if is not written, fails when input is all negetive.
    if Max_sum<0:
        return Max_sum

    return Max_circular_sum

def majorityElement(array):
    """
    Given an array, return all indices of majority elements. Najority element is that which has occurerd more than n/2 times in the array where n is length of array.

    Dict Method:
        Space: O(n)
        Time : O(n)
    
    Sort Method:
        Space: O(1)
        Time: O(n)
    """
    
    # # Dict method
    # res = {}
    # n = len(array)
    # for i in range(len(array)):
    #     curr = array[i]
    #     if curr in res.keys():
    #         res[curr].append(i)
    #     else:
    #         res[curr] = [i]

    # vals = list(res.values())
    
    # for index_list in vals:
    #     if len(index_list) > n/2:
    #         print(index_list)


def main():
    array = [8,3,4,8,8]
    # print(f"Max difference is : {MaxDifference(array)}")
    # print(f'Max Frequencies in a sorted array : {FreqInSortedArray(array)}')
    #print(f"Max profit : {stockBuySellOne(array)}")
    #print(f"Max rain water strored :  {TrappingRainWater(array)} units")
    #print(f"Maximum consecutinve ones : {maxConsecutiveOnes(array)}")
    #print(MaxSumSubarray(array))
    #print(MaxLengthEvenOdd(array))
    #print(MaxSumCircular(array))
    majorityElement(array)


if __name__ == '__main__':
    main()