import numpy as np

def get_a_row(ci_idx, row_idx):
    res = 0
    for i in range(tile_wi, 0, -1):
        res = (res << 8) + input[ci_idx-1][row_idx-1][i-1]

    return res

tile_wi = 64
tile_hi = 64
tile_ci = 1
p = 2
s = 2
pixels_in_word = 32
buffer_num = 3
buffer_size = 3072

## how to map a or a tile of f_map from ddr to buffers on-chip

# input = [[[11,12,13,14,15,16,17,18],
#          [21,22,23,24,25,26,27,28],
#          [31,32,33,34,35,36,37,38],
#          [41,42,43,44,45,46,47,48],
#          [51,52,53,54,55,56,57,58],
#          [61,62,63,64,65,66,67,68],
#          [71,72,73,74,75,76,77,78],
#          [81,82,83,84,85,86,87,88]]]

input = np.random.rand(tile_ci, tile_hi, tile_wi)
input = input * 256
input = (input-128).astype(np.int8)

buffers = np.zeros((buffer_num, buffer_size)).astype(int)
buffer_ofts = np.zeros((buffer_num)).astype(int)

for ci_i in range(1, tile_ci+1):
    ## fill the north pad from ddr to buffer on chip
    buffer_last_idx = -1
    buffer_last_si = -1
    buffer_last_not_fin = 0
    pad_north_i = 1
    buf_i = 1
    while pad_north_i <= p:
        s_i = 1
        while s_i <= s: ## a buffer need s continuous rows 
            if pad_north_i <= p:
                for pixel_idx in range(1, tile_wi+1, pixels_in_word):
                    print("pad row %d [%d : %d] fill in buffer %d at offset %d" 
                          %(pad_north_i, pixel_idx+pixels_in_word-1, pixel_idx, buf_i, buffer_ofts[buf_i-1]))
                    buffers[buf_i-1][buffer_ofts[buf_i-1]] = 0
                    buffer_ofts[buf_i-1] = buffer_ofts[buf_i-1] + 1
                pad_north_i = pad_north_i + 1
            else:
                buffer_last_not_fin = 1
                buffer_last_idx = buf_i
                buffer_last_si = s_i
                assert s_i > 1 ## need fix [s_i, s] of [1, s]
            s_i = s_i + 1
        buf_i = (buf_i % buffer_num) + 1


    row_i = 1
    ## fix the unfulled tail with fm rows, assert fm rows are enough

    if buffer_last_not_fin == 1:
        buf_i = buffer_last_idx
        s_i = buffer_last_si
        while s_i <= s: ## a buffer need s continuous rows 
            for pixel_idx in range(1, tile_wi+1, pixels_in_word):
                print("fm row %d [%d : %d] fill in buffer %d at offset %d" 
                      %(row_i, pixel_idx+pixels_in_word-1, pixel_idx, buf_i, buffer_ofts[buf_i-1]))
                buffers[buf_i-1][buffer_ofts[buf_i-1]] = get_a_row(ci_idx=ci_i, row_idx=row_i)
                buffer_ofts[buf_i-1] = buffer_ofts[buf_i-1] + 1
            row_i = row_i + 1
            s_i = s_i + 1
        buf_i = (buf_i % buffer_num) + 1

    ## fill the rest fm row from ddr to buffers on chip
    buffer_last_idx = -1
    buffer_last_si = -1
    buffer_last_not_fin = 0
    while row_i <= tile_hi:
        s_i = 1
        while s_i <= s: ## a buffer need s continuous rows 
            if row_i <= tile_hi:
                for pixel_idx in range(1, tile_wi+1, pixels_in_word):
                    print("fm row %d [%d : %d] fill in buffer %d at offset %d" 
                          %(row_i, pixel_idx+pixels_in_word-1, pixel_idx, buf_i, buffer_ofts[buf_i-1]))
                    buffers[buf_i-1][buffer_ofts[buf_i-1]] = get_a_row(ci_idx=ci_i, row_idx=row_i)
                    buffer_ofts[buf_i-1] = buffer_ofts[buf_i-1] + 1
                row_i = row_i + 1
            else:
                buffer_last_not_fin = 1
                buffer_last_idx = buf_i
                buffer_last_si = s_i
                assert s_i > 1 ## need fix [s_i, s] of [1, s]
            s_i = s_i + 1
        buf_i = (buf_i % buffer_num) + 1


    pad_south_i = 1
    ## fix the unfulled tail with south pad rows, assert south pad rows are enough

    if buffer_last_not_fin == 1:
        buf_i = buffer_last_idx
        s_i = buffer_last_si
        while s_i <= s: ## a buffer need s continuous rows 
            for pixel_idx in range(1, tile_wi+1, pixels_in_word):
                print("pad row %d [%d : %d] fill in buffer %d at offset %d" 
                      %(pad_south_i, pixel_idx+pixels_in_word-1, pixel_idx, buf_i, buffer_ofts[buf_i-1]))
                buffers[buf_i-1][buffer_ofts[buf_i-1]] = 0
                buffer_ofts[buf_i-1] = buffer_ofts[buf_i-1] + 1
            pad_south_i = pad_south_i + 1
            s_i = s_i + 1
        buf_i = (buf_i % buffer_num) + 1

    ## fill the south pad
    buffer_last_idx = -1
    buffer_last_si = -1
    buffer_last_not_fin = 0
    while pad_south_i <= p:
        s_i = 1
        while s_i <= s: ## a buffer need s continuous rows 
            if pad_south_i <= p:
                for pixel_idx in range(1, tile_wi+1, pixels_in_word):
                    print("pad row %d [%d : %d] fill in buffer %d at offset %d"
                           %(pad_south_i, pixel_idx+pixels_in_word-1, pixel_idx, buf_i, buffer_ofts[buf_i-1]))
                    buffers[buf_i-1][buffer_ofts[buf_i-1]] = 0
                    buffer_ofts[buf_i-1] = buffer_ofts[buf_i-1] + 1
                pad_south_i = pad_south_i + 1
            else:
                buffer_last_not_fin = 1
                buffer_last_idx = buf_i
                buffer_last_si = s_i
                assert s_i > 1 ## need fix [s_i, s] of [1, s]
            s_i = s_i + 1
        buf_i = (buf_i % buffer_num) + 1