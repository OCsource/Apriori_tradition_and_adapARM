import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
# 导入内部函数

# 定义所需要拟合的带参数的一般函数类型
# 参数：方程式参数
# 返回方程式
def fmax(x, a, b, c, d):
    return a + b*x + c*x*x + d*x*x*x

# 求拟合函数
# 参数：初始候选集及个数（list(tuple)）
# 返回定义的函数中除x外各个参数的值(list)
def func(DoubleList):

    lenX = len(DoubleList) + 1
    # 输入数据x,y
    x = np.arange(1, lenX, 1)
    tempList = []
    for k in DoubleList:
        tempList.append(k[1])   # 取元组的第二项，即每个事物对应的个数
    y = np.array(tempList)
    # 拟合曲线的x
    x1 = np.arange(1, lenX, 0.01)

    '''
    参数分别为函数一般形式、横坐标范围、纵坐标范围、
    返回两个数组，第一个是定义的函数中除x外各个参数的值，第二个是协方差
    '''
    # 最后的数组是对所求函数除x外参数的大小限制#求a,b,c,d
    fita, fitb = optimize.curve_fit(fmax, x, y, [1, 1, 1, 1])

    # 绘图
    # # 输出方程的常量参数
    # plt.plot(x, y)
    # # 画出原来实际数据的图形#
    # plt.plot(x1, fmax(x1, fita[0], fita[1], fita[2], fita[3]))
    # # 画出拟合后获得曲线的图形#
    # plt.show()
    return fita

# 求函数的二阶倒数 + 求解
# 参数：定义的函数中除x外各个参数的值(list)
# 返回x结果，以及原方程式
def derivFunc(fita):
    tempList = []
    for v in fita:
        tempList.insert(0,v)
    p0 = np.poly1d(tempList)
    p = p0.deriv()
    p = p.deriv()
    x0 = (p.coeffs[1] * - 1) / p.coeffs[0]
    return x0,p0

# 调用函数
# 参数：第一个为字典列表key:为名称value:为统计数
# 返回：flag == 0 时：返回二次求导等于零求解值X0，否则返回原方程求解值（X = x0）
def main(DoubleList, flag=0):
    fita = func(DoubleList)
    x0,p0 = derivFunc(fita)
    if flag == 0:
        return x0
    else :
        return p0([x0])