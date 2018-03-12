# 残品折半  从小到大
def halfUp(li,data):
    mid = len(li) // 2
    if li[mid] > data : # 中间数字大于要查找数字 向左边查找
        for i in range(mid-1,0,-1):
            if li[i] == data:
                return i
        return 'errorLeft'
    elif li[mid] == data:
        return mid
    else:#否则向右边查找
        for i in range(mid+1,len(li)):
            if li[i] == data:
                return i
        return 'errorRight'

# 残品折半  从大到小 10 9 8 7 6 5 4 3 2 1
def halfDown(li, data):
    mid = len(li) // 2
    if li[mid] > data:
        for i in range(mid+1,len(li)):
            if li[i] == data:
                return i
        return 'errorRight'
    elif li[mid] == data:
        return mid
    else:
        for i in range(mid-1,0,-1):
            if li[i] == data:
                return i
        return 'errorLeft'

# 标准折半查找 升序序列查找
def FullhalfUp(li,data):
    low = 0
    high = len(li)
    while low <= high:
        mid = (low + high)//2
        if li[mid] == data:
            return mid
        elif li[mid] > data:
            high = mid - 1
        else:
            low = mid + 1
    return -1

# 标准折半查找 降序序列查找
def FullhalfDown(li,data):
    low = 0
    high = len(li)
    while low <= high:
        mid = (low + high)//2
        if li[mid] == data:
            return mid
        elif li[mid] < data:
            high = mid - 1
        else:
            low = mid + 1
    return -1


if __name__ =='__main__':
    li = [1, 2, 3, 4, 5, 7, 9]
    # li = [10,9,8,7,6,5,4,3,2,1]
    findFunc = halfUp
    print(findFunc(li,4))