# This is a sample Python script.


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import conv

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
    config = 2 ## 0, 1, 2, 3

    pox = 4
    poy = 6
    ix = 12
    iy = 12

    k = [1,3,3,6]
    s = [1,1,2,2]
    p = [0,1,1,2]

    k_config = k[config]
    s_config = s[config]
    p_config = p[config]

    ox = conv.out(ix, k_config, s_config, p_config)
    oy = conv.out(iy, k_config, s_config, p_config)
    tile_num_x,left_x,tile_num_y,left_y = conv.tiling(ox, oy, pox, poy)


    # [1...poy]                                   [1...pox] * tile_num_x, [ox-left_x+1, ox] * 1
    # [poy+1...2poy]                              [1...pox] * tile_num_x, [ox-left_x+1, ox] * 1
    # ....
    # [tile_num_y*poy-poy+1...tile_num_y*poy]     [1...pox] * tile_num_x, [ox-left_x+1, ox] * 1
    # [tile_num_y*poy+1...tile_num_y*poy+left_y]  [1...pox] * tile_num_x, [ox-left_x+1, ox] * 1
    for tile_y in range(1, tile_num_y+2):
        if tile_y < tile_num_y + 1:
            for tile_x in range(1, tile_num_x+1):
                print()
                print("tile_y: %d, tile_x: %d, pox: %d, poy: %d" % (tile_y, tile_x, pox, poy))
                conv.conv_tile(ox_start=1+(tile_x-1)*pox, oy_start=1+(tile_y-1)*poy, pox=pox, poy=poy,
                               k=k_config, s=s_config, p=p_config, ix=ix, iy=iy)
            if left_x > 0:
                tile_x = tile_num_x + 1
                print()
                print("tile_y: %d, tile_x: %d, pox: %d, poy: %d" % (tile_y, tile_x, left_x, poy))
                conv.conv_tile(ox_start=1 + (tile_x - 1) * pox, oy_start=1 + (tile_y - 1) * poy, pox=pox, poy=poy,
                               k=k_config, s=s_config, p=p_config, ix=ix, iy=iy)
        elif left_y > 0:
            for tile_x in range(1, tile_num_x + 1):
                print()
                print("tile_y: %d, tile_x: %d, pox: %d, poy: %d" % (tile_y, tile_x, pox, left_y))
                conv.conv_tile(ox_start=1 + (tile_x - 1) * pox, oy_start=1 + (tile_y - 1) * poy, pox=pox, poy=left_y,
                               k=k_config, s=s_config, p=p_config, ix=ix, iy=iy)
            if left_x > 0:
                tile_x = tile_num_x + 1
                print()
                print("tile_y: %d, tile_x: %d, pox: %d, poy: %d" % (tile_y, tile_x, left_x, left_y))
                conv.conv_tile(ox_start=1 + (tile_x - 1) * pox, oy_start=1 + (tile_y - 1) * poy, pox=pox, poy=left_y,
                               k=k_config, s=s_config, p=p_config, ix=ix, iy=iy)





