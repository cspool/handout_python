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
    config = 3 ## 0, 1, 2, 3

    pox = 32 ## parallel output pixels in parallel 
    poy = 3
    ox = 32
    oy = 32

    k = [1,3,3,6]
    s = [1,1,2,2]
    p = [0,1,1,2]

    k_config = k[config]
    s_config = s[config]
    p_config = p[config]

    # ox = conv.out(ix, k_config, s_config, p_config)
    # oy = conv.out(iy, k_config, s_config, p_config)

    ix = conv.input(ox, k_config, s_config, p_config)
    iy = conv.input(oy, k_config, s_config, p_config)

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
    
            print("tile_y_start: %d, tile_x_start: %d, pox: %d, poy: %d"
                  % (tile_y_start, tile_x_start, size_x, size_y))
            conv.conv_tile(ox_start=tile_x_start, oy_start=tile_y_start, pox=pox, poy=size_y,
                           k=k_config, s=s_config, p=p_config, ix=ix, iy=iy)
