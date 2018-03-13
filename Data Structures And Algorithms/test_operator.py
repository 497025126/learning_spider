# -*- coding:utf-8 -*-
# 根据k值的 从大到小排序
import operator
li = [{"k":1,"v":2},{"k":12,"v":22},{"k":13,"v":1}]
li.sort(key=operator.itemgetter('k'),reverse=True)
print(li)
