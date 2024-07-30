import numpy as np
import math

kw = 1 #1, 3, 6
kh = 1 #1, 3, 6

stride = 1 # 1, 2
pad = 0 # 0, 1, 2

ci = 256 # 3, 256, 512...
co = 256 # 3, 256, 512...
wi = 32 # 32, 64, 128, 256, 512, 1024
hi = 32 # 32, 64, 128, 256, 512, 1024

wo = math.floor((wi + 2 * pad - kw) / stride) + 1
ho = math.floor((hi + 2 * pad - kh) / stride) + 1

tile_ci = 16 # memory transaction and dataflow 
parallel_ci = 1 # parrallel computation, fixed

tile_co = 128 # 128 in precision of 1/8, 64 in precision of 8/8, can enhance
parallel_co = 128 # fixed

tile_wo = 32 # can enhance
parallel_wo = 32 # fixed

tile_ho = 3 # can enhance
parallel_ho = 3 #fixed


weights = np.random.rand(co, ci, kh, kw)
input= np.random.rand(ci, hi, wi)

out_tile_unroll = np.zeros((co, ho, wo))

out = np.zeros((co, ho, wo))

for tile_ci_i in range(1, ci+1, tile_ci):
    #tile_ci index
    tile_ci_size = min(tile_ci, ci+1-tile_ci_i)

    for tile_co_i in range(1, co+1, tile_co):
        #tile_co index
        tile_co_size = min(tile_co, co+1-tile_co_i)

        for tile_ho_i in range(1, ho+1, tile_ho):
            #tile_ho index
            # some tile_ho may not eq 3
            tile_ho_size = min(tile_ho, ho+1-tile_ho_i)
        
            for tile_wo_i in range(1, wo+1, tile_wo):
                #tile_wo index
                tile_wo_size = min(tile_wo, wo+1-tile_wo_i)

                for kw_i in range(1,kw+1):
                    #kw index

                    for kh_i in range(1,kh+1):
                        #kh index

                        for ci_parallel_index in range(tile_ci_i, tile_ci_i + tile_ci_size, parallel_ci):
                            # ci_i is computed in parallel_ci
                            parallel_ci_size = min(parallel_ci, tile_ci_i + tile_ci_size -ci_parallel_index)

                            for co_parallel_index in range(tile_co_i, tile_co_i + tile_co_size, parallel_co):
                                # co_i is computed in parallel_co
                                parallel_co_size = min(parallel_co, tile_co_i + tile_co_size -co_parallel_index)

                                for ho_parallel_index in range(tile_ho_i, tile_ho_i + tile_ho_size, parallel_ho):
                                    # ho_i is computed in parallel_ho
                                    parallel_ho_size = min(parallel_ho, tile_ho_i + tile_ho_size -ho_parallel_index)

                                    for wo_parallel_index in range(tile_wo_i, tile_wo_i+tile_wo_size, parallel_wo):
                                        # wo_i is computed in parallel_wo
                                        parallel_wo_size = min(parallel_wo, tile_wo_i + tile_wo_size -wo_parallel_index)

                                        for ci_i in range(ci_parallel_index, ci_parallel_index + parallel_ci_size):
                                            

                                            for co_i in range(co_parallel_index, co_parallel_index + parallel_co_size):
                                                

                                                for ho_i in range(ho_parallel_index, ho_parallel_index + parallel_ho_size):
                                                    

                                                    for wo_i in range(wo_parallel_index, wo_parallel_index+parallel_wo_size):
                                        
                                                        wi_i = (wo_i - 1) * stride + kw_i

                                                        hi_i = (ho_i - 1) * stride + kh_i
                                                        

                                                        out_tile_unroll[co_i-1][ho_i-1][wo_i-1] += \
                                                        input[ci_i-1][hi_i-1][wi_i-1] * weights[co_i-1][ci_i-1][kh_i-1][kw_i-1]


## conventional convolution

for ci_i in range(1, ci+1):
    #tile_ci index

    for co_i in range(1, co+1):
        #tile_co index

        for ho_i in range(1, ho+1):
            #tile_ho index
        
            for wo_i in range(1, wo+1):
                #tile_wo index

                for kw_i in range(1,kw+1):
                    #kw index

                    for kh_i in range(1,kh+1):
                        #kh index

                        wi_i = (wo_i - 1) * stride + kw_i

                        hi_i = (ho_i - 1) * stride + kh_i
                                        
                        out[co_i-1][ho_i-1][wo_i-1] += \
                                        input[ci_i-1][hi_i-1][wi_i-1] * weights[co_i-1][ci_i-1][kh_i-1][kw_i-1]
                        
                



print(np.array_equal(out_tile_unroll, out))

print("end")


'''

conv(...)

pseudo_code:

for kw_i in range(1,kw+1):
    #kw index

    for kh_i in range(1,kh+1):
        #kh index

        for tile_ci_i in range(1, ci+1, tile_ci):
            #tile_ci index
            tile_ci_size = min(tile_ci, ci+1-tile_ci_i)

            for tile_co_i in range(1, co+1, tile_co):
                #tile_co index
                tile_co_size = min(tile_co, co+1-tile_co_i)

                for tile_ho_i in range(1, ho+1, tile_ho):
                    #tile_ho index
                    # some tile_ho may not eq 3
                    tile_ho_size = min(tile_ho, ho+1-tile_ho_i)
                
                    for tile_wo_i in range(1, wo+1, tile_wo):
                        #tile_wo index
                        tile_wo_size = min(tile_wo, wo+1-tile_wo_i)

                        for ci_parallel_index in range(tile_ci_i, tile_ci_i + tile_ci_size, parallel_ci):
                            parallel_ci_size = min(parallel_ci, tile_ci_i + tile_ci_size -ci_parallel_index)
                            
                            # ci_i is computed in parallel_ci_size

                            for co_parallel_index in range(tile_co_i, tile_co_i + tile_co_size, parallel_co):
                                parallel_co_size = min(parallel_co, tile_co_i + tile_co_size -co_parallel_index)
                                
                                # co_i is computed in parallel_co_size

                                for ho_parallel_index in range(tile_ho_i, tile_ho_i + tile_ho_size, parallel_ho):
                                    parallel_ho_size = min(parallel_ho, tile_ho_i + tile_ho_size -ho_parallel_index)
                                    
                                    # ho_i is computed in parallel_ho_size

                                    for wo_parallel_index in range(tile_wo_i, tile_wo_i+tile_wo_size, parallel_wo):
                                        parallel_wo_size = min(parallel_wo, tile_wo_i + tile_wo_size -wo_parallel_index)
                                        
                                        # wo_i is computed in parallel_wo_size
                                        
                                        wi_i = (wo_i - 1) * stride + kw_i
                                        hi_i = (ho_i - 1) * stride + kh_i

                                        out_tile_unroll[co_i-1][ho_i-1][wo_i-1] += \
                                        input[ci_i-1][hi_i-1][wi_i-1] * weights[co_i-1][ci_i-1][kh_i-1][kw_i-1]

'''
                    
'''
E_scale(A, E_scale_tail, scale_rank)
input [8*32*2*3-1 :0] A;
input [8 + 7:0]E_scale_tail;
input [5:0]scale_rank; //[-63, 0]

output [(8+1)*192-1:0]
map(lambda: i->(clamp((A[8*i+7:8*i] * E_scale_tail * 2^scale_rank), -256,255), range(0, 32*2*3))

乘方用移位实现.
预计使用192个DSP.
'''

'''
shortcut-concate(A, scale1_tail, scale1_rank, B, scale2_tail, scale2_rank)
input [8*256-1 :0] A;
input [7:0]scale1_tail;
input [4:0]scale1_rank; //[-31, 0];

input [8*256-1 :0] B;
input [7:0]scale2_tail;
input [4:0]scale2_rank; //[-31, 0];

output [(8+1)*256-1:0]
map(lambda: i->clamp((E_scale(A[8*i+7:8*i], scale1_tail, scale1_rank) +
                       E_scale(B[8*i+7:8*i], scale2_tail, scale2_rank), -256, 255)), range(0, 256))

这里的E_scale只表示运算,需要单独用DSP实现,而非复用上面的E_scale模块.
预计使用256个DSP,每个DSP能实现2个8bit和8bit的乘法.
'''

'''
relu
input [(8+1)*256-1 :0] A;

output [8*256-1:0]map(lambda: i->(clamp(relu(A[9*i+8:9*i]), 0, 255)), range(0, 256))

'''

'''
pool
pseudo_code:


'''