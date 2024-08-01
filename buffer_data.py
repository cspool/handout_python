import numpy as np

paths = ['./rom1.txt', './rom2.txt', './rom3.txt']

def get_a_row(ci_idx, row_idx, col_l, col_r, pad):
    res = ''
    if pad:
            res = '0'
    else:
        for i in range(col_r, col_l-1, -1):
            ele = input[ci_idx-1][row_idx-1][i-1]
            ele = ele if ele >= 0 else (ele+256)
            s_ele = format(ele, '02X')
            res = res + s_ele
    return res

config = 3
k           = [1, 3, 3, 6] ## useless
s_set       = [1, 1, 2, 2]
p_set       = [0, 1, 1, 2]
tile_wi_set = [32,32,64,64]
tile_hi_set = [32,32,16,16]

tile_wi = tile_wi_set[config]
tile_hi = tile_hi_set[config]
tile_ci = 256
p = p_set[config]
s = s_set[config]
pixels_in_word = 32
buffer_num = 3
buffer_size = 5120

## how to map a or a tile of f_map from ddr to buffers on-chip
input = np.zeros((tile_ci, tile_hi, tile_wi)).astype(np.int8)

if config == 0 or config == 1:
    ## 32 * 32
    input_row1 = np.arange(0, 32)
    input_row2 = np.arange(32, 64)
    input_row3 = np.arange(64, 96)
    input_row4 = np.arange(96, 128)
    input_row5 = np.arange(128, 160)
    input_row6 = np.arange(160, 192)
    input_row7 = np.arange(192, 224)
    input_row8 = np.arange(224, 256)

    for tci in range(1, tile_ci+1):
        for thi in range(1, tile_hi, 8):
            input[tci-1][thi-1] = input_row1
            input[tci-1][thi-1 + 1] = input_row2
            input[tci-1][thi-1 + 2] = input_row3
            input[tci-1][thi-1 + 3] = input_row4
            input[tci-1][thi-1 + 4] = input_row5
            input[tci-1][thi-1 + 5] = input_row6
            input[tci-1][thi-1 + 6] = input_row7
            input[tci-1][thi-1 + 7] = input_row8
else:
    ## 64 * 64
    input_row1 = np.arange(0, 64)
    input_row2 = np.arange(64, 128)
    input_row3 = np.arange(128, 192)
    input_row4 = np.arange(192, 256)

    for tci in range(1, tile_ci+1):
        for thi in range(1, tile_hi, 4):
            input[tci-1][thi-1] = input_row1
            input[tci-1][thi-1 + 1] = input_row2
            input[tci-1][thi-1 + 2] = input_row3
            input[tci-1][thi-1 + 3] = input_row4


# input = np.random.rand(tile_ci, tile_hi, tile_wi)
# input = input * 256
# input = (input-128).astype(np.int8)

buffers = np.full((buffer_num, buffer_size), "0", dtype=object)
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
                    buffers[buf_i-1][buffer_ofts[buf_i-1]] = \
                        get_a_row(ci_idx=ci_i, row_idx=pad_north_i, col_l=pixel_idx, col_r=pixel_idx+pixels_in_word-1, pad=1)
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
                buffers[buf_i-1][buffer_ofts[buf_i-1]] = \
                    get_a_row(ci_idx=ci_i, row_idx=row_i, col_l=pixel_idx, col_r=pixel_idx+pixels_in_word-1, pad=0)
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
                    buffers[buf_i-1][buffer_ofts[buf_i-1]] = \
                        get_a_row(ci_idx=ci_i, row_idx=row_i, col_l=pixel_idx, col_r=pixel_idx+pixels_in_word-1, pad=0)
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
                buffers[buf_i-1][buffer_ofts[buf_i-1]] = \
                    get_a_row(ci_idx=ci_i, row_idx=pad_south_i, col_l=pixel_idx, col_r=pixel_idx+pixels_in_word-1, pad=1)
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
                    buffers[buf_i-1][buffer_ofts[buf_i-1]] = \
                        get_a_row(ci_idx=ci_i, row_idx=pad_south_i, col_l=pixel_idx, col_r=pixel_idx+pixels_in_word-1, pad=1)
                    buffer_ofts[buf_i-1] = buffer_ofts[buf_i-1] + 1
                pad_south_i = pad_south_i + 1
            else:
                buffer_last_not_fin = 1
                buffer_last_idx = buf_i
                buffer_last_si = s_i
                assert s_i > 1 ## need fix [s_i, s] of [1, s]
            s_i = s_i + 1
        buf_i = (buf_i % buffer_num) + 1

for buf_i in range(1, buffer_num+1):
    # 打开文件用于写入（'w' 模式），如果文件不存在将会被创建
    with open('/Users/zack/Desktop/PythonPros/handout/' + paths[buf_i-1], 'w') as file:
        # 使用 write() 方法写入字符串
        file.write("MEMORY_INITIALIZATION_RADIX = 16 ;\n")
        file.write("MEMORY_INITIALIZATION_VECTOR =\n")
        for buf_oft in range(1, buffer_size+1):
            file.write(buffers[buf_i-1][buf_oft-1])
            if buf_oft == buffer_size:
                file.write(";\n")
            else:
                file.write(",\n")