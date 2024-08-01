import numpy as np
import math

## idx    1  2 ... p  p+1 ... p+ix p+ix+1 ... p+ix+p
##  1     0  0     0  0        0    0          0
##  2     0  0     0  0        0    0          0
##  .     0  0     0  x        x    0          0
##  .     0  0     0  x        x    0          0
##  p     0  0     0  x        x    0          0
## p+1    0  0     0  x        x    0          0
##  .     0  0     0  x        x    0          0
##  .     0  0     0  x        x    0          0
##p+iy    0  0     0  x        x    0          0
##p+iy+1  0  0     0  0        0    0          0
##  .     0  0     0  0        0    0          0
##  .     0  0     0  0        0    0          0
##p+iy+p  0  0     0  0        0    0          0

def out(input, k, s, p):
    ## (out - 1)*s +k = in + 2p
    return math.floor((input + 2*p - k)/s + 1)

def input(out, k, s, p):
    return (out - 1) * s + k - 2*p

# [1...poy]                                   [1...pox] * tile_num_x, [ox-left_x+1, ox] * 1
# [poy+1...2poy]                              [1...pox] * tile_num_x, [ox-left_x+1, ox] * 1
# ....
# [tile_num_y*poy-poy+1...tile_num_y*poy]     [1...pox] * tile_num_x, [ox-left_x+1, ox] * 1
# [tile_num_y*poy+1...tile_num_y*poy+left_y]  [1...pox] * tile_num_x, [ox-left_x+1, ox] * 1

def tiling(ox, oy, pox, poy):
    tile_num_x = math.floor(ox/pox)
    tile_num_y = math.floor(oy/poy)
    left_x = ox - tile_num_x * pox
    left_y = oy - tile_num_y * poy
    return tile_num_x, left_x, tile_num_y, left_y

def conv_row_tile(row_y, ix, ox_start, pox, k, s, p): ##ox, oy are from 1
    ## imap[ix_start, ix_end], imap[iy_start, iy_end_min], they are from 1
    ix_start = (ox_start - 1) * s + 1
    ## ix_start = (1+(tile_x-1)*pox - 1)*s+1=(tile_x-1)*s*pox+1
    ix_end = ix_start + (pox - 1) * s + k - 1
    ## ix_end = (tile_x-1)*s*pox+1+pox*s-s+k-1=tile_x*s*pox+k-s
    ix_end_min = ix_start + (pox - 1) * s + 1 + 1 - 1
    ## ix_end_min = (tile_x-1)*s*pox+1+pox*s-s+1=tile_x*s*pox+2-s
    if ix_end_min > ix_end: ## k = 1
        ix_end_min = ix_end

    left_pad = (p - ix_start + 1) if (ix_start <= p) else 0
    right_pad = (ix_end - (p + ix)) if (ix_end > (p + ix)) else 0
    right_pad_min = (ix_end_min - (p + ix)) if (ix_end_min > (p + ix)) else 0

    row_start = ix_start + left_pad
    # row_start [1...ix+2p]
    if (row_start > ix + p):
        exit(-1)
    row_start = row_start - p - 1
    # row_start [0...ix-1]
    # row_start = 0 if (ix_start <= p) else (tile_x)*s*pox - p

    row_end_min = ix_end_min - right_pad_min
    # row_end_min [1...ix+2p]
    if (row_end_min < 1):
        exit(-1)
    row_end_min = row_end_min - p - 1
    # row_end_min [0...ix-1]
    # row_end_min = ix-1 if (ix_end_min - (p + ix) > 0) else (tile_x+1)*s*pox -p -s+1

    row_end = ix_end - right_pad
    # row_end [1...ix+2p]
    if (row_end < 1):
        exit(-1)
    row_end = row_end - p - 1
    # row_end [0...ix-1]
    # row_end = ix-1 if (ix_end - (p + ix) > 0) else (tile_x+1)*s*pox+ k-s-p-1

    # left_pad, row[row_start, row_end_min], row[row_end_min+1, row_end], right_pad

    overlap = 0 if (row_start == 0) else p

    assert overlap + left_pad == p

    assert math.ceil(row_start/pox) * pox == row_start + overlap

    row_start = math.ceil(row_start/pox) * pox

    # left_pad, overlap, row[r_s, r_e_m], row[r_e_m+1, r_e], p
    row_end_min = min(math.ceil(row_end_min / pox) * pox - 1, ix-1)
    row_end = min(math.ceil(row_end / pox) * pox - 1, ix-1)

    # left_pad, overlap, row[r_s, r_e_m], row[r_e_m+1, r_e], p

    print("0*%d, slab*%d, row%d[%d, %d], row%d[%d, %d], 0*%d"
          %(left_pad, overlap, row_y, row_start, row_end_min, row_y, row_end_min+1, row_end, p))

    # left_pad, overlap ----> reg[1, from-1]
    reg_from = left_pad + overlap + 1

    # left_pad, overlap ----> reg[1, from-1]
    print("%d  0*%d, slab*%d into reg[%d]-reg[%d]"
          % (1, left_pad, overlap, 1, reg_from - 1))

    # row[r_s, r_e_m] ----> reg[from, to]
    cycle = 1
    reg_to = -1
    for adr in range(row_start, row_end_min+1, pox):
        reg_to = reg_from + row_end_min - adr if (adr + pox - 1 > row_end_min) else reg_from + pox - 1
        # row[adr, adr2] ----> reg[from+(i-1)*pox, to]
        print("%d  row%d[%d:%d] into reg[%d]-reg[%d]"
         % (cycle, row_y, adr, adr + pox - 1, reg_from, reg_to))
        cycle = cycle + 1
        reg_from = reg_to + 1

    # row[r_e_m+1, r_e] ----> reg[to, end]
    # right_pad ----> reg[to, end]

    min_reg = reg_to
    max_reg = max(reg_to, reg_to + row_end - row_end_min - 1, reg_to + p - 1)
    # row[r_e_m+1, r_e] ----> reg[to, end]
    for adr in range(row_end_min + 1, row_end + 1, pox):
        reg_end = reg_to + row_end - adr if (adr + pox - 1 > row_end) else reg_to + pox - 1
        print("%d  row%d[%d:%d] into reg[%d]-reg[%d]"
         % (cycle, row_y, adr, adr+pox-1, reg_to, reg_end))
        cycle = cycle + reg_end - reg_to + 1

    # 0*p ----> reg[to, end]
    print("%d  0*%d into reg[%d]-reg[%d]"
          % (cycle, p, reg_to, reg_to + p - 1))

def conv_tile(ox_start, oy_start, pox, poy, k, s, p, ix, iy):
    iy_start = (oy_start - 1) * s + 1
    iy_last_start = iy_start + (poy - 1) * s
    # start_row indexes of poy data_routers
    for irow_y in range(iy_start, iy_last_start+1, s):
        print("---------------------------------")
        for ky in range(irow_y, irow_y+k):
            ky = -1 if (ky < p + 1 or ky > p + iy) else ky-p
            conv_row_tile(row_y=ky, ix=ix, ox_start=ox_start, pox=pox, k=k, s=s, p=p)