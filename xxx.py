from data_in_systolic_array import to_hex_twos_complement
def useless_func(tofill, content):
# temporary ref_type var tofill(val=ref of tofill outside),content(val=ref of content outside) is created when enter the func,
# and the equation op assign the val of var content(the ref of the obj content outside) to the temporary var tofill,
# which means that tofill ref to the content obj outside the func after assign
# however, the tofill is a temporary var and is destroyed with its ref nums == 0 when leave the func
# and the nums in obj tofill never change
    print("in useless func")
    print("tofill")
    print(id(tofill))
    print(tofill)
    print("content")
    print(id(content))
    print(content)
    tofill = content
    print("tofill")
    print(id(tofill))
    print(tofill)  
    print("content")
    print(id(content))
    print(content)


def useful_func(tofill, content):
# a temporary ref_type var tofill,content is created when enter the func,
# and the extend func of the obj(the tofill obj outside the func) that the tofill ref is called
# the extend func copy the numbers in obj content(var content refs) to the obj that tofill refs
    print("in useful func")
    print("tofill")
    print(id(tofill))
    print(tofill)
    print("content")
    print(id(content))
    print(content)
    tofill.extend(content)
    print("tofill")
    print(id(tofill))
    print(tofill)
    print("content")
    print(id(content))
    print(content)


# content = [1,2,3]
# tofill=[]
# print("before enter func:")
# print("tofill")
# print(id(tofill))
# print(tofill)
# print("content")
# print(id(content))
# print(content)
#
# useless_func(tofill, content)
# print("outside useless func:")
# print(tofill)
#
# useful_func(tofill, content)
# print("outside useful func:")
# print(tofill)
#
# tofill = []
# print("outside the tofill is a obj")
# print(tofill)
# tofill = content
# print(tofill)

# demo_list = []
# demo_list.extend([0]*0)
# print(demo_list)
#
# demo_list = demo_list.extend([0]*0) ## extend return none
# print(demo_list)

print(to_hex_twos_complement((((-62*104)&0xfffff) + (((-62*124) & 0xfffff) << 20)
                              + (((-62 * 18)&0xfffff) << 40) + (((-62*125)&0xfffff) << 60)), 80))

print(to_hex_twos_complement((((-60*104)&0xfffff) + (((-60*124) & 0xfffff) << 20)
                              + (((-60*18) & 0xfffff) << 40) + (((-60*125) & 0xfffff) << 60)), 80))

print(to_hex_twos_complement((((-64)&0x3fff) + (((19) & 0x3fff) << 20)
                              + (((-16)&0x3fff) << 40) + (((55)&0x3fff) << 60)), 80))

print(to_hex_twos_complement((((64)&0x3fff) + (((-19) & 0x3fff) << 20)
                              + (((16) & 0x3fff) << 40) + (((-55) & 0x3fff) << 60)), 80))