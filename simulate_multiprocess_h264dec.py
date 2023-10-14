import os
import multiprocessing
import time
from itertools import product

GEM5PATH= "/gem5/build/ARM"
SCRIPTPATH= "/gem5/configs/simulations-cpu/CortexA76"
WORKLOADS= "/gem5/configs/simulations-cpu/ARM_workloads"

def process1(i): 
    MOREOPTIONS= "--l1i_size="+combs[i][0]+" --l1d_size="+combs[i][1]+" --l2_size="+combs[i][2]+" --l3_size="+combs[i][3]+" --rob_entries="+str(combs[i][4])+" --btb_entries="+str(combs[i][5])+" --num_fu_FP_SIMD_ALU="+str(combs[i][6])+" --issue_width="+str(combs[i][7])
    OUTDIR = "/gem5/m5out_multiprocess_h264_dec/h264_dec_l1i_size="+combs[i][0]+"_l1d_size="+combs[i][1]+"_l2_size="+combs[i][2]+"_l3_size="+combs[i][3]+"_rob="+str(combs[i][4])+"_btb="+str(combs[i][5])+"_num_ALU="+str(combs[i][6])+"_issue_width="+str(combs[i][7])
    command = GEM5PATH+"/gem5.opt "+" --outdir="+OUTDIR+" "+SCRIPTPATH+"/CortexA76.py --cmd="+WORKLOADS+"/h264_dec/h264_dec --options=\""+WORKLOADS+"/h264_dec/h264dec_testfile.264 h264dec_outfile.yuv\" "+MOREOPTIONS
    # command = GEM5PATH+"/gem5.opt "+SCRIPTPATH+"/CortexA76.py --cmd="+WORKLOADS+"/mp3_enc/mp3_enc --options=\""+WORKLOADS+"/mp3_enc/mp3enc_testfile.wav mp3enc_outfile.mp3\" "+MOREOPTIONS
    print(command+"\n")
    returned = os.system(command)
    if returned != 0:
        print("Hubo un error al ejecutar el comando.")

# Para obtener posibles combinaciones
l1i_size = ["32kB","64kB"]
l1d_size = ["32kB","64kB"]
l2_size = ["128kB","256kB","512kB"]
l3_size = ["2MB","8MB","16MB"] 
rob_entries = [192, 256]
btb_entries = [8192, 16384]
num_ALU = [2, 3]
issue_width = [8, 12]
combs = list(product(l1i_size, l1d_size, l2_size, l3_size, rob_entries, btb_entries, num_ALU, issue_width))
# for comb_i in combs:
#     print(comb_i)

if __name__ == "__main__":
    processes = 12
    index = range(processes) # Tiene que ser un vector
    
    begin_list = 454
    end_list = 454+12 #len(combs)  
    print("\nComenzando simulacion concurrente. Tiempo estimado: ",((end_list-begin_list)/processes)*37/60," horas\n")  
    
    start_time = time.time()
    for list_block in range(begin_list, end_list, processes):             
        start_block_t = time.time()
        pool = multiprocessing.Pool(processes)        
        index = range(list_block, list_block + processes)
        pool.map(process1, index)
        pool.close()
        pool.join()       
        # print(list_block)
        # print(index)  
        end_block_t = time.time()-start_block_t
        print("Ejecucion de bloque ["+str(list_block)+","+str(list_block+processes-1)+"] terminada en", end_block_t/60," min\n")  
    
    end_time = time.time()-start_time
    print("Simulacion completa, duracion: ", end_time/60," min\n")
        
        
        
        
        
        