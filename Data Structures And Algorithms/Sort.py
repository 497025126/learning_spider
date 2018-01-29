# 冒泡排序
# 升序
def BubbleUp(li):
    for i in range(1,len(li)):
        for j in range(0,len(li)-i):
            if li[j] > li[j+1]:
                li[j],li[j+1] = li[j+1],li[j]

# 降序
def BubbleDown(li):
    # i 的值是每次比较完之后队列减少的数量
    for i in range(1,len(li)):
        for j in range(0,len(li)-i):
            if li[j] < li[j+1]:
                li[j],li[j+1] = li[j+1],li[j]

# 选择排序 降序
def selectDown(li):
    for i in range(1, len(li)):
        min_index = 0
        for n in range(0, len(li)-i+1):
            if li[min_index] > li[n]:
                min_index = n
        li[min_index], li[len(li) - i] = li[len(li) - i], li[min_index]
    return li

# 选择排序 升序
def selectUp(li):
    for i in range(1,len(li)):
        max_index = 0
        for j in range(0,len(li)-i+1):
            if li[max_index] < li[j]:
                max_index = j
        li[max_index],li[len(li)-i] = li[len(li)-i],li[max_index]
    return li

# 插入排序 降序
def insertSort(li):
    if len(li) <= 1:
        return
    pos = 0
    for i in range(1,len(li)):
        temp = li[i]
        for n in range(i,0,-1):
            if li[n-1] < temp:
                li[n] = li[n-1]
            else:
                pos = n
                break
        li[pos] = temp

# 快速排序
def QuickSort(li,low,high):
    if low > high:
        return
    # 设置哨兵
    pivotkey = li[low]
    l = low
    h = high
    while l < h:
        while (l < h) and li[h] >= pivotkey:
            h -= 1

        li[l] = li[h]
        while (l < h) and li[l] <= pivotkey:
            l += 1
        li[h] = li[l]

    li[l] = pivotkey
    QuickSort(li,low,high-1)
    QuickSort(li,low+1,high)

if __name__ == '__main__':
    l = [9,1,7,4,3,5,3,4,2]
    # l = [9,8,7,6,5,4,3,2,1_tcp,0]
    sort_func = QuickSort
    sort_func(l,0,len(l)-1)
    print(l)