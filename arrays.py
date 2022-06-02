import math
from tempfile import TemporaryDirectory


def largestInAnArray(array):
    """
    Return the largest element on the array.

    Complexity:
        space: O[1]
        time: O(n)
    """

    MAX = -math.inf

    for i in range (len(array)):
        if array[i] > MAX:
            MAX = array[i]

    return MAX


def secondLargestElement(array):
    """
    Return index of the second largest element.
    Complexity:
        Space: O[1]
        Time = O(n)
    """

    if len(array)<2:
        return -1

    largest =  0
    second = -math.inf

    for i in range(len(array)):
        if array[i] > array[largest]:
            second = largest
            largest = i

        elif array[i] < array[largest]:
            if second == -math.inf:
                second = i
            elif array[i] > array[second]:
                second = i
    return second

def checkSorted(array):
    """
    Check if an array is sorted(increasing order) or not.
    Complexity:
        space: O(1)
        time: O(n)
    """

    if len(array) < 2:
        return True

    for i in range(1,len(array)):
        if array[i] < array[i-1]:
            return False

    return True

def reverseArray(array):
    """
    Reverse an array in place.
    Complexity:
        Space: O(1)
        Time: O(n)
    """
    if len(array) == 0:
        return -1

    i = 0
    j = len(array)-1

    # while i < j:
    #     temp = array[i]
    #     array[i] = array[j]
    #     array[j] = temp
    #     i+=1
    #     j-=1

    # Without temp variable
    while i<j:
        array[i],array[j] = array[j],array[i]
        i+=1
        j-=1
    return array

def removeDuplicatesInSortedArray(array):
    """
    Remove duplicates in sorted array.
    Complexity:
        space : O(1)
        Time: O(n)
    """

    if len(array)==0:
        return -1

    # Compare every element to element at pos. If same, continue. If different, increment pos and copy the new distince elemnt. Pos always holds index of last distince element.
    # pos = 0
    # for i in range(len(array)):
    #     if array[i] != array[pos]:
    #         pos +=1
    #         array[pos] = array[i]
    
    # for i in range(pos+1,len(array)):
    #     array[i] = '_'

    # OR

    # Compare every subsequent elements. And do the same.
    res = 1
    for i in range(1,len(array)):
        if array[i]!=array[i-1]:
            array[res] = array[i]
            res+=1
    
    for i in range(res,len(array)):
        array[i] = '_'
    
    return array

def moveZeroToEnd(array):
    """
    Move all 0s to end of the array
    Complexity:
        space : O(1)
        Time: O(n)
    """

    if len(array) == 0:
        return -1

    # Traverse every element. If it is zero, i++. If non zero, copy element i to pos, i++ and pos ++.
    pos = 0
    for i in range(len(array)):
        if array[i]!=0:
            array[pos] = array[i]
            pos +=1
    
    for i in range(pos,len(array)):
        array[i] = 0

    return array

def leftRotateOne(array):
    """
    Left rotate array by 1
    Complexity:
        space : O(1)
        Time: O(n)
    """
    temp = array[0]
    for i in range(1,len(array)):
        array[i-1] = array[i]

    array[-1] = temp

    return array

def leftRotateD(array,d):
    """
    Rotate an element by D position to the left
    Naive: 
      Space: O(1), 
      Time O(nd)
    
    Better: 
        Space: O(d), 
        time : O(n)
    
    Best:
        Time: O(n), 
        space: O(1)
    """
    

    # NAIVE approach: Nested Loop

    # for i in range(d):
    #     temp = array[0]
    #     for j in range(1,len(array)):
    #         array[j-1] = array[j]
    #     array[-1] = temp

    # BETTER approach:  Store 1st d elements in temp array. Move remaining elements by d pos. Copy temp array to end of array.
    # temp_array = array[:d]
    # for i in range(d, len(array)):
    #     array[i-d] = array[i]

    # index = len(array) - d
    # i = 0 
    # while index < len(array):
    #     array[index] = temp_array[i]
    #     i+=1
    #     index+=1

    # BEST approach: Reversal technique
    array[:d] = array[:d][::-1]     # reverse 1st d elements in place
    array[d:] = array[d:][::-1]     # reverse remaining n-d elements in place
    array = array[::-1]             # reverse entire array
    return array

def rightRotateD(array,d):
    pass

def leaderInArray(array):
    """
    Print leader in an array. Leader is any element which does not have any greater or equal element on its right side. 
    Eg: Input = [7,10,4,3,6,5,2] -> Ouput = 10,6,5,2
    Complexity:
        Space = O(1)
        Time = O(n)
    """
    # Set last elemetn as MAX. Traverse from the right. if any element is strictly greater than MAX, print it and update MAX.
    i = len(array) - 2
    MAX = array[-1]
    print(MAX)

    while i>=0:
        if array[i] > MAX:
            MAX = array[i]
            print(array[i])
        i-=1


def main():
    array = [7,10,4,3,6,5,2]
    #print(f"Largest element in the array is: ",largestInAnArray(array))
    #print(f"Second Largest element : ", secondLargestElement(array))
    #print(f"Is the array sorted? : ",checkSorted(array))
    #print(f"Reverse of an array: ", reverseArray(array))
    #print(removeDuplicatesInSortedArray(array))
    #print(moveZeroToEnd(array))
    #print(leftRotateOne(array))
    #print(leftRotateD(array,3))
    print("Leader in the Array :",leaderInArray(array))

    





if __name__ == '__main__':
    main()