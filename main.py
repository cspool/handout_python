# This is a sample Python script.


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import conv
import math

## idx    1  2 ... p  p+1 ... p+ix p+ix+1 ... p+ix+p
##  1     0  0     0  0        0    0          0
##  2     0  0     0  0        0    0          0
##  .     0  0     x  x        x    0          0
##  .     0  0     x  x        x    0          0
##  p     0  0     x  x        x    0          0
## p+1    0  0     x  x        x    0          0
##  .     0  0     x  x        x    0          0
##  .     0  0     x  x        x    0          0
##p+iy    0  0     x  x        x    0          0
##p+iy+1  0  0     x  x        x    0          0
##  .     0  0     0  0        0    0          0
##  .     0  0     0  0        0    0          0
##p+iy+p  0  0     0  0        0    0          0

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    config = 3 ## 0, 1, 2, 3

    pox = 32 ## parallel output pixels in parallel 
    poy = 3
    
    
    k = [1,3,3,6]
    s = [1,1,2,2]
    p = [0,1,1,2]

    k_config = k[config]
    s_config = s[config]
    p_config = p[config]


    ox = 32
    oy = 32

    ix = 128 
    iy = 128

    # ox = conv.out(ix, k_config, s_config, p_config)
    # oy = conv.out(iy, k_config, s_config, p_config)

    tile_x_start = 1
    tile_y_start = 1

    # # maybe scan x direction first, then y direction
    # for tile_y_start in range(1, oy+1, poy):
    #     # [tile_y_start, tile_y_start+poy-1]
    #     size_y = oy - tile_y_start + 1 if(tile_y_start+poy-1 > oy) else poy

    #     for tile_x_start in range(1, ox+1, pox):
    #         # [tile_x_start, tile_x_start+pox-1]
    #         size_x = ox - tile_x_start + 1 if(tile_x_start+pox-1 > ox) else pox

    #         print("tile_y_start: %d, tile_x_start: %d, pox: %d, poy: %d"
    #               % (tile_y_start, tile_x_start, size_x, size_y))
    #         conv.conv_tile(ox_start=tile_x_start, oy_start=tile_y_start, pox = pox, poy=size_y,
    #                        k=k_config, s=s_config, p=p_config, ix=ix, iy=iy)

    for tile_x_start in range(1, ox + 1, pox):
        # [tile_x_start, tile_x_start+pox-1]
        size_x = ox - tile_x_start + 1 if (tile_x_start + pox - 1 > ox) else pox
    
        for tile_y_start in range(1, oy + 1, poy):
            # [tile_y_start, tile_y_start+poy-1]
            size_y = oy - tile_y_start + 1 if (tile_y_start + poy - 1 > oy) else poy

            # compute a tile of an out channel
            print("tile_y_start: %d, tile_x_start: %d, pox: %d, poy: %d"
                  % (tile_y_start, tile_x_start, size_x, size_y))
            conv.conv_tile(ox_start=tile_x_start, oy_start=tile_y_start, pox=size_x, poy=size_y,
                           k=k_config, s=s_config, p=p_config, ix=ix, iy=iy)


'''
module conv_tiling

for tile_x_start in range(1, ox + 1, pox):
    # [tile_x_start, tile_x_start+pox-1]
    size_x = ox - tile_x_start + 1 if (tile_x_start + pox - 1 > ox) else pox

    for tile_y_start in range(1, oy + 1, poy):
        # [tile_y_start, tile_y_start+poy-1]
        size_y = oy - tile_y_start + 1 if (tile_y_start + poy - 1 > oy) else poy

        # compute a tile of an out channel
        print("tile_y_start: %d, tile_x_start: %d, pox: %d, poy: %d"
                % (tile_y_start, tile_x_start, size_x, size_y))
        conv.conv_tile(ox_start=tile_x_start, oy_start=tile_y_start, pox=pox, poy=size_y,
                        k=k_config, s=s_config, p=p_config, ix=ix, iy=iy)

'''


'''
module conv_tile

def conv_tile(ox_start, oy_start, pox, poy, k, s, p, ix, iy):
    iy_start = (oy_start - 1) * s + 1
    iy_last_start = iy_start + (poy - 1) * s
    
    # router 1
    irow_y1 = iy_start
    while irow_y1 <= iy_last_start:
        print("----------------- router %d ctrl serial ----------------" %(1))
        for kyi in range(0, k):
            ky = -1 if ((kyi + irow_y1) < p + 1 or (kyi + irow_y1) > p + iy) else kyi + irow_y1 -p
            conv_row_tile(row_y=ky, ix=ix, ox_start=ox_start, pox=pox, k=k, s=s, p=p)
        irow_y1 = irow_y1 + s * poy

    # router 2
    irow_y2 = iy_start + s
    while irow_y2 <= iy_last_start:
        print("----------------- router %d ctrl serial ----------------" %(2))
        for kyi in range(0, k):
            ky = -1 if ((kyi + irow_y2) < p + 1 or (kyi + irow_y2) > p + iy) else kyi + irow_y2 -p
            conv_row_tile(row_y=ky, ix=ix, ox_start=ox_start, pox=pox, k=k, s=s, p=p)
        irow_y2 = irow_y2 + s * poy

    # router 3
    irow_y3 = iy_start + s + s
    while irow_y3 <= iy_last_start:
        print("----------------- router %d ctrl serial ----------------" %(3))
        for kyi in range(0, k):
            ky = -1 if ((kyi + irow_y3) < p + 1 or (kyi + irow_y3) > p + iy) else kyi + irow_y3 -p
            conv_row_tile(row_y=ky, ix=ix, ox_start=ox_start, pox=pox, k=k, s=s, p=p)
        irow_y3 = irow_y3 + s * poy

'''


'''
module conv_row

def conv_row_tile(row_y, ix, ox_start, pox, k, s, p): ##ox, oy are from 1
    ix_start = (ox_start - 1) * s + 1
                    
    ix_end = ix_start + (pox - 1) * s + k - 1
    
    ix_end_min = ix_start + (pox - 1) * s + 1 + 1 - 1 if ix_end_min <= ix_end else ix_end

    left_pad = (p - ix_start + 1) if (ix_start <= p) else 0
    right_pad = (ix_end - (p + ix)) if (ix_end > (p + ix)) else 0
    right_pad_min = (ix_end_min - (p + ix)) if (ix_end_min > (p + ix)) else 0

    overlap = 0 if (ix_start <= p + 1) else p
    
    row_start = ix_start + left_pad - p - 1 + overlap

    row_end_min = ix_end_min - right_pad_min - p - 1

    row_end = ix_end - right_pad - p - 1

    row_end_min = min(math.ceil(row_end_min / pox) * pox - 1, ix-1)
    row_end = min(math.ceil(row_end / pox) * pox - 1, ix-1)

    print("0*%d, slab*%d, row%d[%d, %d], row%d[%d, %d], 0*%d"
        %(left_pad, overlap, row_y, row_start, row_end_min, row_y, row_end_min+1, row_end, p))

    reg_from = left_pad + overlap + 1

    print("%d  0*%d, slab*%d into reg[%d]-reg[%d]"
        % (1, left_pad, overlap, 1, reg_from - 1))

    cycle = 1
    reg_to = -1
    for adr in range(row_start, row_end_min+1, pox):
        reg_to = reg_from + row_end_min - adr if (adr + pox - 1 > row_end_min) else reg_from + pox - 1
        print("%d  row%d[%d:%d] into reg[%d]-reg[%d]"
        % (cycle, row_y, adr, adr + pox - 1, reg_from, reg_to))
        cycle = cycle + 1
        reg_from = reg_to + 1

    min_reg = reg_to
    max_reg = max(reg_to, reg_to + row_end - row_end_min - 1, reg_to + p - 1)
    for adr in range(row_end_min + 1, row_end + 1, pox):
        reg_end = reg_to + row_end - adr if (adr + pox - 1 > row_end) else reg_to + pox - 1
        print("%d  row%d[%d:%d] into reg[%d]-reg[%d]"
        % (cycle, row_y, adr, adr+pox-1, reg_to, reg_end))
        cycle = cycle + reg_end - reg_to + 1

    print("%d  0*%d into reg[%d]-reg[%d]"
        % (cycle, p, reg_to, reg_to + p - 1))


'''

'''
module mononithic conv

    for tile_x_start in range(1, ox + 1, pox):
        size_x = ox - tile_x_start + 1 if (tile_x_start + pox - 1 > ox) else pox
    
        for tile_y_start in range(1, oy + 1, poy):
            size_y = oy - tile_y_start + 1 if (tile_y_start + poy - 1 > oy) else poy
            
            iy_start = (tile_y_start - 1) * s_config + 1
            iy_last_start = iy_start + (size_y - 1) * s_config
            for irow_y in range(iy_start, iy_last_start+1, s_config):
                print("---------------------------------")
                for ky in range(irow_y, irow_y+k_config):
                    ky = -1 if (ky < p_config + 1 or ky > p_config + iy) else ky-p_config                    
                    
                    ix_start = (tile_x_start - 1) * s_config + 1
                    
                    ix_end = ix_start + (pox - 1) * s_config + k_config - 1
                    
                    ix_end_min = ix_start + (pox - 1) * s_config + 1 + 1 - 1
                    
                    if ix_end_min > ix_end:
                        ix_end_min = ix_end

                    left_pad = (p_config - ix_start + 1) if (ix_start <= p_config) else 0
                    right_pad = (ix_end - (p_config + ix)) if (ix_end > (p_config + ix)) else 0
                    right_pad_min = (ix_end_min - (p_config + ix)) if (ix_end_min > (p_config + ix)) else 0

                    overlap = 0 if (ix_start <= p_config + 1) else p_config
                    
                    row_start = ix_start + left_pad - p_config - 1 + overlap
            
                    row_end_min = ix_end_min - right_pad_min - p_config - 1

                    row_end = ix_end - right_pad - p_config - 1

                    row_end_min = min(math.ceil(row_end_min / pox) * pox - 1, ix-1)
                    row_end = min(math.ceil(row_end / pox) * pox - 1, ix-1)

                    print("0*%d, slab*%d, row%d[%d, %d], row%d[%d, %d], 0*%d"
                        %(left_pad, overlap, ky, row_start, row_end_min, ky, row_end_min+1, row_end, p_config))

                    reg_from = left_pad + overlap + 1

                    print("%d  0*%d, slab*%d into reg[%d]-reg[%d]"
                        % (1, left_pad, overlap, 1, reg_from - 1))

                    cycle = 1
                    reg_to = -1
                    for adr in range(row_start, row_end_min+1, pox):
                        reg_to = reg_from + row_end_min - adr if (adr + pox - 1 > row_end_min) else reg_from + pox - 1
                        print("%d  row%d[%d:%d] into reg[%d]-reg[%d]"
                        % (cycle, ky, adr, adr + pox - 1, reg_from, reg_to))
                        cycle = cycle + 1
                        reg_from = reg_to + 1

                    min_reg = reg_to
                    max_reg = max(reg_to, reg_to + row_end - row_end_min - 1, reg_to + p_config - 1)
                    for adr in range(row_end_min + 1, row_end + 1, pox):
                        reg_end = reg_to + row_end - adr if (adr + pox - 1 > row_end) else reg_to + pox - 1
                        print("%d  row%d[%d:%d] into reg[%d]-reg[%d]"
                        % (cycle, ky, adr, adr+pox-1, reg_to, reg_end))
                        cycle = cycle + reg_end - reg_to + 1

                    print("%d  0*%d into reg[%d]-reg[%d]"
                        % (cycle, p_config, reg_to, reg_to + p_config - 1))

#'''


