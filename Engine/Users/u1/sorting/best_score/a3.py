import numpy as np
def bubbleSort(arr):
    n = len(arr)

    # Traverse through all array elements
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
    x = arr
    for i in range(0,1000):
        for j in range(0,10000):
            x = 3*x
        if i % 2==0:
            x = x*5
        else:
            x = x+100

# Driver code to test above
arr = [64, 34, 25, 12, 22, 11, 90]
arr = np.asarray(arr)
bubbleSort(arr)
for i in range(len(arr)):
    print ("%d" %arr[i]),
