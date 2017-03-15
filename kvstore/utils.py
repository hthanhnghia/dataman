# find the maximum value in the array 'arr' that is less than or equal to 'val'
def lower_bound(arr, val):
    ans = None
    if len(arr) > 0:
        for x in arr:
            if x > ans and x <= val:
                ans = x
    return ans