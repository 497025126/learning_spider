# -*- coding:utf-8 -*-
# 冒泡排序
def bubble_sort(li):
    # 每轮把最大or最小值找出来
    for i in range(1,len(li)):
        for j in range(0,len(li)-i):
            if li[j] > li[j+1]: # 大于号 升序 小于号 降序
                li[j+1],li[j] = li[j],li[j+1]

# 选择排序
def select_sort(li):
    # 每次选出当前区间内最小or最大的和内层区间最后一个交换交换
    for i in range(1,len(li)):
        index = 0
        for j in range(0,len(li)-i+1):
            # 大于号  找出最小的值 索引
            if li[index] > li[j]:
                index = j
        li[index],li[len(li)-i] = li[len(li)-i],li[index]

# 插入排序 不能有重复数字
def insert_sort(li):
    for i in range(1,len(li)):
        temp = li[i]
        for j in range(i,0,-1):
            pos = 0
            if li[j-1] < temp: #降序
                li[j] = li[j-1]
            else:
                pos = j
                break
        li[pos] = temp

# 快速排序
def QuickSort(li,low,high):
    # 递归跳出条件
    if low > high:
        return
    sentry = li[low]
    l = low
    h = high
    while l < h:
        while (l < h) and li[h] >= sentry:
            h -= 1
        li[l],li[h] = li[h],li[l]
        while (l < h) and li[l] <= sentry:
            l += 1
        li[l],li[h] = li[h],li[l]
    li[l] = sentry
    QuickSort(li, low, high - 1)
    QuickSort(li, low + 1, high)

# 希尔排序 缩小增量排序
def ShellSort(li):
   step = len(li) // 2
   while step > 0:
       for i in range(step,len(li)):
           while i >= step and li[i-step]>li[i]:
               li[i-step],li[i] = li[i],li[i-step]
               i -= step
       step = step // 2

#  堆排序
def HeapSort(li):
    pass

# 归并排序
def MergeSort(li):
    """
    :param li:要求传入的序列基本有序
    :return:新序列
    """
    liLeft = li[:len(li)//2]
    liRight = li[len(li)//2:]
    l = r = 0
    newli = []
    while l < len(liLeft) and r < len(liRight):
        if liLeft[l] < liRight[r]:
            newli.append(liLeft[l])
            l += 1
        else:
            newli.append(liRight[r])
            r += 1
    if l == len(liLeft):
        for temp in liRight[r:]:
            newli.append(temp)
    else:
        for temp in liLeft[l:]:
            newli.append(temp)
    return newli
# 基数排序
def BaseSort(li):
    pass


if __name__ == '__main__':
    li = [5,3,6,7,4,2,1,9,7,10]
    # sort_method = ShellSort
    # sort_method(li)
    # QuickSort(li,0,len(li)-1)
    # print(li)
    # new = MergeSort(li)
    # print(new)
