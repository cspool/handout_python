import math
import random

def to_hex_twos_complement(number, bits=16):
    """将有符号整数转换为16进制补码形式。

    Args:
    numbers: 有符号整数。
    bits: 整数的位数，默认为8位。

    Returns:
    一个16进制数。
    """
    mask = (1 << bits) - 1
    if number < 0:
        twos_complement = (number + (1 << bits)) & mask
    else:
        twos_complement = number & mask
    return hex(twos_complement)

def get_pixel(feature_maps, channel, x, y, nix, niy, p): ##channel, x, y from 1
    if (x >= 1 + p and x <= nix+p and y >= 1+p and y <= niy+p):
        x = x - p
        y = y - p
        return feature_maps[(channel-1) * nix * niy + (y-1)*nix + (x-1)]

    else:
        return 0

def get_weight(kernels,kernel_id, channel, x, y, nkx, nky, nif): ##channel, x, y from 1
    return kernels[(kernel_id-1)*nkx*nky*nif + (channel-1)*nkx*nky + (y-1)*nkx + x-1]

def generate_conv_data(feature_maps, kernels, rearranged_fm, rearranged_k,nix, niy, nkx, nky, s, p, nif, nof):
    nox = math.floor((nix+2*p-nkx)/s + 1)
    noy = math.floor((niy+2*p-nky)/s + 1)

    for oy in range(1, noy+1):
        if len(rearranged_fm) < noy:
            rearranged_fm.append([])
        else:
            rearranged_fm[oy-1]=[]
        for ox in range(1, nox+1):
            if len(rearranged_fm[oy-1]) < nox:
                rearranged_fm[oy-1].append([])
            else:
                rearranged_fm[oy - 1][ox-1] = []
            x_origin = (ox-1)*s+1
            y_origin = (oy-1)*s+1
            for tf in range(1, nif+1):
                for ky in range(1, nky+1):
                    for kx in range(1, nkx+1):
                        x = x_origin + kx-1
                        y = y_origin + ky-1
                        rearranged_fm[oy-1][ox-1].append(get_pixel(feature_maps, tf, x, y, nix, niy, p))


    for of in range(1, nof+1):
        if len(rearranged_k) < nof:
            rearranged_k.append([])
        else:
            rearranged_k[of-1] = []
        for tf in range(1, nif+1):
            for ky in range(1, nky+1):
                for kx in range(1, nkx+1):
                    rearranged_k[of-1].append(get_weight(kernels=kernels,kernel_id=of,
                                                         channel=tf, x=kx, y=ky, nkx=nkx, nky=nky, nif=nif))

def init_fm_k(feature_maps, kernels, nif, nix, niy, nkx, nky, nof, israndom, fm_word_width, ker_word_width):
    fm_max_value = 2 ** (fm_word_width - 1) - 1
    fm_min_value = -2 ** (fm_word_width - 1)

    ker_max_value = 2 ** (ker_word_width - 1) - 1 if ker_word_width > 1 else 1
    ker_min_value = -2 ** (ker_word_width - 1) if ker_word_width > 1 else 0

    for i in range(1, nif+1): ## 3 channels
        for j in range(1, niy+1): ## 9 rows
            for k in range(1, nix+1): ## 9 columns
                if israndom:
                    feature_maps.append(random.randint(fm_min_value, fm_max_value))
                else:
                    feature_maps.append(i * 100 + j * 10 + k)

    for c in range(1, nof+1): ## 9 kernels
        for i in range(1, nif+1): ## 3 channels
            for j in range(1, nky+1): ## nky=3
                for k in range(1, nkx+1): ## nkx=3
                    if israndom:
                        kernels.append(random.randint(ker_min_value, ker_max_value))
                    else:
                        kernels.append(c*1000 + i * 100 + j * 10 + k)

# a big mononithic tiling
def monolithic_bit_fusion(mode, re_fm, re_ker, fused_fm, fused_ker, nof, nox, noy):
    # fuse 2 activation(8 bits) in a word(16 bits / 8 bits)
    for oy in range(1, noy + 1):
        if len(fused_fm) < noy:
            fused_fm.append([])
        else:
            fused_fm[oy - 1] = []

        is_even = 1
        if nox & 0x1 == 0x1:
            is_even = 0
        for ox in range(1, nox + 1, 2):
            if len(fused_fm[oy - 1]) < math.ceil(nox/2):
                fused_fm[oy - 1].append([])
            else:
                fused_fm[oy - 1][math.ceil(ox/2) - 1] = []
            # re_fm[oy-1][ox-1],re_fm[oy-1][ox+1-1]
            assert is_even == 0 or len(re_fm[oy-1][ox-1]) == len(re_fm[oy-1][ox+1-1])
            for i in range(1, len(re_fm[oy-1][ox-1])+1):
                a1 = re_fm[oy-1][ox-1][i-1] ## signed value, lower ox index fused in the lower bits
                a2 = (re_fm[oy-1][ox+1-1][i-1]) if (is_even == 1 or ox +1 < nox+1) else 0 ## signed value, higher ox index fused in the higher bits
                fused_fm[oy-1][math.ceil(ox/2) - 1].append((a2 << 8) + a1)



    if mode == 0: ## 1 weight(8 bits) in a word(8 bits)
        fused_ker.extend(re_ker)
    else: ## fuse 2 weight(1 bits) in a word(8 bits)
        is_even = 1
        if nof & 0x1 == 0x1:
            is_even = 0

        for of in range(1, nof+1, 2):
            if len(fused_ker) < math.ceil(nof/2):
                fused_ker.append([])
            else:
                fused_ker[math.ceil(of/2)-1] = []
            assert is_even == 0 or len(re_ker[of-1]) == len(re_ker[of+1-1])
            for i in range(1, len(re_ker[of-1])+1):
                w1 = re_ker[of-1][i-1] ## signed value, lower channel index fused in the lower bits
                w2 = (re_ker[of+1-1][i-1]) if is_even == 1 or of < nof else 0 ## signed value, higher channel index fused in the higher bits
                fused_ker[math.ceil(of/2)-1].append((w2 << 1) + w1)

## row_num = pof = tof, column_num = pox = tox, sa_num = poy = toy
    #
    # for bof in range(1, nof+1, tof):
    #     for boy in range(1, noy+1, toy):
    #         for box in range(1, nox+1, tox):
    #
    #             for of in range(bof, bof + tof):
    #                 for oy in range(boy, boy + toy):
    #                     for ox in range(box, box+tox):
def tiling_bit_fusion(mode, re_fm, re_ker, tilings_fused_fm, tilings_fused_ker,
                   tox, tof, toy, nof, noy, nox,
                      zero_switch):
    tile_num_oy = math.ceil(noy/toy)
    for boy in range(1, noy + 1, toy):
        boy_by_toy = math.ceil(boy/toy) ## boy_by_toy is the index of tile_y_index, a tile_oy once
        if len(tilings_fused_fm) < tile_num_oy:
            tilings_fused_fm.append([])
        else:
            tilings_fused_fm[boy_by_toy - 1] = []

        tile_num_ox = math.ceil(nox / tox)
        for box in range(1, nox + 1, tox):
            box_by_tox = math.ceil(box / tox) ## box_by_tox is the index of tile_x(fm), a tile_ox once
            if len(tilings_fused_fm[boy_by_toy - 1]) < tile_num_ox:
                tilings_fused_fm[boy_by_toy - 1].append([])
            else:
                tilings_fused_fm[boy_by_toy - 1][box_by_tox - 1] = []

            end_oy = min(boy + toy, noy + 1)-1
            size_a_oy_tile = end_oy - boy + 1
            for oy in range(boy, end_oy+1):
                oy_in_tile = (oy-1)%toy + 1 ## oy_in_tile is in [1,3], map to 3 SAs
                if len(tilings_fused_fm[boy_by_toy - 1][box_by_tox - 1]) < size_a_oy_tile:
                    tilings_fused_fm[boy_by_toy - 1][box_by_tox - 1].append([])
                else:
                    tilings_fused_fm[boy_by_toy - 1][box_by_tox - 1][oy_in_tile-1] = []

                end_ox = min(box + tox, nox + 1) - 1
                size_a_ox_tile = math.ceil((end_ox - box + 1) / 2)
                is_even = 1
                if size_a_ox_tile & 0x1 == 0x1:
                    is_even = 0
                # a num in fused_fm is 2 activation
                for ox in range(box, end_ox+1, 2):
                    ox_in_tile=math.ceil((((ox-1)%tox) +1)/2) ## ox_in_tile is in [1, column_num], map to those columns
                    if len(tilings_fused_fm[boy_by_toy - 1][box_by_tox - 1][oy_in_tile-1]) < size_a_ox_tile:
                        tilings_fused_fm[boy_by_toy - 1][box_by_tox - 1][oy_in_tile-1].append([])
                    else:
                        tilings_fused_fm[boy_by_toy - 1][box_by_tox - 1][oy_in_tile-1][ox_in_tile-1]= []
                    # zero extension
                    zero_num = ox_in_tile-1 if zero_switch else 0
                    # add zero_num zero
                    tilings_fused_fm[boy_by_toy - 1][box_by_tox - 1][oy_in_tile-1][ox_in_tile-1].extend([0]*zero_num)

                    assert is_even == 0 or len(re_fm[oy - 1][ox - 1]) == len(re_fm[oy - 1][ox + 1 - 1])
                    for i in range(1, len(re_fm[oy - 1][ox - 1]) + 1):
                        a1 = re_fm[oy - 1][ox - 1][i - 1]  ## signed value, lower ox index fused in the lower bits
                        a2 = (re_fm[oy - 1][ox + 1 - 1][i - 1]) if (
                                    is_even == 1 or ox +1 < end_ox) else 0  ## signed value, higher ox index fused in the higher bits
                        tilings_fused_fm[boy_by_toy - 1][box_by_tox - 1][oy_in_tile-1][ox_in_tile-1].append((a2 << 8) + a1)

                    zero_num = (size_a_ox_tile - zero_num - 1) if zero_switch else 0
                    tilings_fused_fm[boy_by_toy - 1][box_by_tox - 1][oy_in_tile - 1][ox_in_tile - 1].extend([0]*zero_num)

    tile_size_of = math.ceil(nof/tof)
    for bof in range(1, nof + 1, tof):
        bof_by_tof = math.ceil(bof/tof) ## boy_by_toy is the index of tile_of(ker), a tile_of once
        if len(tilings_fused_ker) < tile_size_of:
            tilings_fused_ker.append([])
        else:
            tilings_fused_ker[bof_by_tof - 1] = []

        of_step = mode + 1 ## 1 if mode == 0; 2 if mode == 1
        end_of = min(bof + tof, nof+1) -1
        size_a_of_tile = math.ceil((end_of - bof + 1) / of_step)
        is_even = 1
        if size_a_of_tile & 0x1 == 0x1:
            is_even = 0
        for of in range(bof, end_of+1, of_step):
            of_in_tile = math.ceil((((of-1)%tof)+1)/of_step)  ## of_in_tile is in [1, row_num], map to those rows
            if len(tilings_fused_ker[bof_by_tof - 1]) < size_a_of_tile:
                tilings_fused_ker[bof_by_tof - 1].append([])
            else:
                tilings_fused_ker[bof_by_tof - 1][of_in_tile - 1] = []

            # zero extension
            zero_num = of_in_tile - 1 if zero_switch else 0
            # add zero_num zero
            tilings_fused_ker[bof_by_tof - 1][of_in_tile - 1].extend([0] * zero_num)

            assert mode == 0 or is_even == 0 or len(re_ker[of - 1]) == len(re_ker[of + 1 - 1])
            for i in range(1, len(re_ker[of - 1]) + 1):
                w1 = re_ker[of - 1][i-1]  ## signed value, lower ox index fused in the lower bits
                w2 = (re_ker[of + 1 - 1][i - 1]) if (
                        mode == 1 and(is_even == 1 or of + 1 < end_of)) else 0  ## signed value, higher ox index fused in the higher bits
                tilings_fused_ker[bof_by_tof - 1][of_in_tile - 1].append((w2 << 1) + w1)

            zero_num = (size_a_of_tile) - zero_num - 1 if zero_switch else 0
            tilings_fused_ker[bof_by_tof - 1][of_in_tile - 1].extend([0]*zero_num)


mode = 1

feature_maps = []

kernels=[]

re_fm=[]

re_kernel = []

fused_fm=[]

fused_ker=[]

tilings_fused_fm=[]
tilings_fused_ker=[]

nix=5;
niy=5;
nif=3;
nof=4;
nkx=3; ## 1 3
nky=3; ## 1 3
s=1; ## 1
p=1; ## 0 1

column_num = 32
row_num = 32
sa_num = 3

tox = 2 * column_num
toy = sa_num
tof = row_num if mode == 0 else 2 * row_num

nox = math.floor((nix+2*p-nkx)/s + 1)
noy = math.floor((niy+2*p-nky)/s + 1)



fm_word_width = 8
ker_word_width = 8 if mode == 0 else 1

fused_fm_bits = 16
fused_ker_bits = 8 if mode == 0 else 1

init_fm_k(feature_maps=feature_maps, kernels=kernels,
          nif=nif, nix=nix, niy=niy, nkx=nkx, nky=nky, nof=nof,
          israndom=True, fm_word_width=fm_word_width, ker_word_width=ker_word_width)

generate_conv_data(feature_maps=feature_maps, kernels=kernels, rearranged_fm=re_fm, rearranged_k=re_kernel,
                   nix=nix, niy=niy, nkx=nkx, nky=nky, s=s, p=p, nif=nif, nof=nof)

print("---------rearranged feature map----------")
for oy in range(1, len(re_fm) + 1):

    for ox in range(1, len(re_fm[oy-1]) + 1):
        print("oy:%d, ox:%d" % (oy, ox))
        print(re_fm[oy-1][ox-1])

print("----------rearranged kernels-------------")

for of in range(1, len(re_kernel) +1):
    print("of:%d" % (of))
    print(re_kernel[of-1])


# monolithic_bit_fusion(mode=mode, re_fm=re_fm, re_ker=re_kernel, fused_fm=fused_fm, fused_ker=fused_ker,
#            nof=nof, nox=nox, noy=noy)
#
# print("---------fused feature map----------")
# for oy in range(1, len(fused_fm) + 1):
#
#     for ox in range(1, len(fused_fm[oy-1]) + 1):
#         hex_numbers = [hex(num) for num in fused_fm[oy-1][ox-1]]
#         print(hex_numbers)
#
# print("----------fused kernels-------------")
#
# for of in range(1, len(fused_ker) +1):
#     bin_numbers = [bin(num) for num in fused_ker[of-1]]
#     print(bin_numbers)

tiling_bit_fusion(mode=mode, re_fm=re_fm, re_ker=re_kernel,
              tilings_fused_fm=tilings_fused_fm, tilings_fused_ker=tilings_fused_ker,
               tox=tox, tof=tof, toy=toy, nof=nof, nox=nox, noy=noy, zero_switch=True)

print("mode %d, zero_ext" %(mode))
print("---------fused tiling feature map----------")
for boy in range(1, len(tilings_fused_fm) + 1):

    for box in range(1, len(tilings_fused_fm[boy-1]) + 1):

        for oy in range(1, len(tilings_fused_fm[boy-1][box-1]) + 1):

            for ox in range(1, len(tilings_fused_fm[boy-1][box-1][oy-1]) + 1):
                print("tile_oy_index:%d, tile_ox_index:%d, oy_in_tile:%d, ox_in_tile:%d" %(boy, box, oy, ox))
                hex_numbers = [to_hex_twos_complement(num, fused_fm_bits) for num in tilings_fused_fm[boy-1][box-1][oy-1][ox-1]]
                print(hex_numbers)

print("----------fused tiling kernels-------------")

for bof in range(1, len(tilings_fused_ker) +1):

    for of in range(1, len(tilings_fused_ker[bof-1]) + 1):
        print("tile_of_index:%d, of_in_tile:%d" % (bof, of))
        hex_numbers = [to_hex_twos_complement(num, fused_ker_bits) for num in tilings_fused_ker[bof-1][of-1]]
        print(hex_numbers)