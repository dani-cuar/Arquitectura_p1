import os
import shutil

# Definir la carpeta principal
carpeta_principal = "/home/user/gem5/m5out_multiprocess_h264_dec_2"

# Ruta de archivos necesarios para generar archivo .xml
archivo1 = "/home/user/gem5/configs/simulations-cpu/gem5_McPAT/ARM_A76_2.1GHz.xml"
archivo2 = "/home/user/gem5/configs/simulations-cpu/gem5_McPAT/gem5toMcPAT_cortexA76.py"

# Recorrer la carpeta principal y sus subcarpetas
count = 0
for directorio_actual, subdirectorios, archivos in os.walk(carpeta_principal):
    subdirectorios.sort()
    for subdirectorio in subdirectorios:
        ruta_completa = os.path.join(carpeta_principal, subdirectorio)
        print(ruta_completa)
        # if(count==2):
        #     break
        # count += 1
        
        # Copiar el archivo
        shutil.copy(archivo1, ruta_completa)
        shutil.copy(archivo2, ruta_completa)
        
        os.chdir(ruta_completa) # Cambiar al directorio actual
        
        command = "python2 gem5toMcPAT_cortexA76.py stats.txt config.json ARM_A76_2.1GHz.xml"
        print(command)
        returned = os.system(command)
        if returned != 0: print("Hubo un error al ejecutar el comando.")
        
        command = "$HOME/mcpat-master/mcpat -infile config.xml > power_data.log"
        print(command)
        returned = os.system(command)
        if returned != 0: print("Hubo un error al ejecutar el comando.")
       
       # ruta_completa = os.path.join(directorio_actual, archivo)







