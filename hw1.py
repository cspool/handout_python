from bisect import bisect_right
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def Fn(x, sample, m):                       #定义函数Fn
    n=len(sample)                           #样本容量n
    f, b=np.histogram(sample, bins=m)       #计算样本分组及频数
    f=f/n                                   #计算各组频率
    ff = [0]
    ff.append(f[0])
    for k in range(m-1):                    #计算累积频率
        f[k+1]+=f[k]
        ff.append(f[k+1])
    y=np.zeros(x.size)                      #函数值初始化为0

    last_index = 0
    for i in range(0, m + 1):
        index = bisect_right(x, b[i])
        if index == x.size:
            index = x.size - 1
        for k in range(last_index, index + 1):
            y[k] = ff[i]
        last_index = index + 1
    for k in range(last_index, x.size):
        y[k] = 1
    return y                                #返回y

def statistics_T(array_z):
    min_z = min(array_z)
    mean_z = sum(array_z) / len(array_z)
    # find the minimum of the array and the sum of it
    res = 0
    for zi in array_z:
        res = res + (zi - mean_z) * (zi - mean_z)

    res = ((res / len(array_z)) ** 0.5) / (mean_z - min_z)

    return res


def mento_carlo(distribution, count_z, count_sample, bins):
    array_T = []
    for i in range(0, count_sample):
        if distribution == 0:  # normal distribution
            array_z = np.random.normal(0, 1, count_z)
        elif distribution == 1:  # exponent distribution
            array_z = np.random.exponential(1.0, count_z)
        else:
            print("unsupported distribution")
            return

        array_T.append(statistics_T(array_z))

    print(pic_path)
    print(np.percentile(array_T, 0.01))
    print(np.percentile(array_T, 0.05))
    print(np.percentile(array_T, 0.1))

    # plt.clf()
    # plt.hist(array_T, bins)
    # plt.savefig(path)
    # plt.show()

    # x = np.linspace(min(array_T), max(array_T), count_sample * 2)
    # plt.clf()
    # plt.plot(x, Fn(x, array_T, bins))
    # plt.savefig(pic_path)
    # plt.show()
