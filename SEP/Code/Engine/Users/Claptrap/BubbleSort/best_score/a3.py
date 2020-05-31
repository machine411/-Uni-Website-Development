import numpy as np
from memory_profiler import *
def bubbleSort(arr):
    n = len(arr)
    a=[1111]*200000000
    # y()
    # Traverse through all array elements
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
    x = arr
    # for i in range(0,1000):
    #     for j in range(0,10000):
    #         x = 3*x
    #     if i % 2==0:
    #         x = x*5
    #     else:
    #         x = x+100

# def y():
#     a=[1111]*9999999
# Driver code to test above

if __name__ == '__main__':
    arr = [64, 34, 25, 12, 22, 11, 90]
    b = [120]*200000000
    arr = np.asarray(arr)
    bubbleSort(arr)

    for i in range(len(arr)):
        print ("%d" %arr[i]),
