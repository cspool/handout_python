def signed_value(value, bits):
    """计算补码表示的有符号值。"""
    if bits == 1:
        return value
    if value & (1 << (bits - 1)):
        value -= (1 << bits)
    return value


def check_conditions(a, b, c, d):
    # 处理4位补码
    a = signed_value(a, 8)
    b = signed_value(b, 8)
    c = signed_value(c, 2)
    d = signed_value(d, 2)

    # 构造L
    L = (c << 20) + signed_value(d & 0x3, 2)
    # 构造R
    R = (a << 10) + signed_value(b & 0xFF, 8)

    # 计算乘积Z
    Z = L * R

    # 输出Z的二进制表示
    print(f"Z的二进制表示: {Z:040b}")

    print(f"Z的[0:9]二进制: {Z & 0b1111111111:010b}")
    print(f"Z的[10:19]二进制: {(Z >> 10) & 0b1111111111:010b}")
    print(f"Z的[20:29]二进制: {(Z >> 20) & 0b1111111111:010b}")
    print(f"Z的[30:39]二进制: {(Z >> 30) & 0b1111111111:010b}")

    # 提取Z的各个部分，并解释为有符号整数
    z_0_9 = signed_value(Z & 0b1111111111, 10)
    z_10_19 = signed_value((Z >> 10) & 0b1111111111, 10)
    z_20_29 = signed_value((Z >> 20) & 0b1111111111, 10)
    z_30_39 = signed_value((Z >> 30) & 0b1111111111, 10)
    z_9 = signed_value((Z >> 9) & 0x1, 1)
    z_19 = signed_value((Z >> 19) & 0x1, 1)
    z_29 = signed_value((Z >> 29) & 0x1, 1)

    # 打印直接乘积结果和Z中的结果
    print("直接乘积 d*b:", d * b)
    print("Z的[0:9]:", z_0_9)
    print("直接乘积 d*a:", d * a)
    print("Z的[10:19]加上Z的第9位:", z_10_19 + z_9)
    print("直接乘积 c*b:", c * b)
    print("Z的[20:29]位加上Z的第19位:", z_20_29 + z_19)
    print("直接乘积 c*a:", c * a)
    print("Z的[29:39]位加上Z的第29位:", z_30_39 + z_29)


# 示例输入
a = 0b01000011  # 67
b = 0b11111100  # -4
c = 0b01  # 1
d = 0b11  # -1

# 执行并打印结果
check_conditions(a, b, c, d)