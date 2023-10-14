import re
import os

def save_cpi(archivo):
    patron = r"system\.cpu\.cpi\s+([\d.]+)"
    
    valor = None
    try:
        with open(archivo, "r") as file:
            for linea in file:
                match = re.search(patron, linea)         
                if match:
                    valor = match.group(1)
                    break
    except FileNotFoundError:
        return "El archivo stats.txt no se encontró en esta carpeta."

    if valor is not None:
        print("Valor CPI guardado es:", valor)
        return valor

def save_power_data(archivo):
    patron_leak = r"Total Leakage = ([\d.]+) W"
    patron_dyn = r"Runtime Dynamic = ([\d.]+) W"

    valor_leak = None
    valor_dyn = None
    try:
        with open(archivo, "r") as file:
            for linea in file:
                match_leak = re.search(patron_leak, linea)
                match_dyn = re.search(patron_dyn, linea)         
                if match_leak:
                    valor_leak = match_leak.group(1)

                if match_dyn:
                    valor_dyn = match_dyn.group(1)
                    break
    except FileNotFoundError:
        return "El archivo power_data.log no se encontró en esta carpeta."

    if valor_leak is not None and valor_dyn is not None:
        print("Valor Total Leakage guardado es:", valor_leak,"y valor Dynamic Power:",valor_dyn)
        return valor_leak, valor_dyn


# Definir la carpeta principal
carpeta_principal = "/home/user/gem5/m5out_multiprocess_mp3_enc"
# carpeta_principal = "/home/user/gem5/m5out_multiprocess_h264_dec"

# Recorrer la carpeta principal y sus subcarpetas
output = []
cpi = 0
return_leak = 0
return_dyn = 0
for directorio_actual, subdirectorios, archivos in os.walk(carpeta_principal):  
    subdirectorios.sort(key= lambda x: int(x.split('_')[0]))
    # print(directorio_actual)
    for archivo in archivos:    
        if archivo == "stats.txt":
            ruta_completa = os.path.join(directorio_actual, archivo)
            cpi = save_cpi(ruta_completa)
        
        if archivo == "power_data.log":
            ruta_completa = os.path.join(directorio_actual, archivo)
            return_leak, return_dyn = save_power_data(ruta_completa)
    subdirectorio_actual = os.path.basename(directorio_actual)
    output.append((cpi, return_leak, return_dyn, subdirectorio_actual))
output.pop(0)
print(len(output))
print(output)

ruta = '/home/user/gem5/configs/simulations-cpu/'
with open(ruta+'output.txt', 'w') as file:
    for i in range(len(output)):
        line = f"{output[i][0]}, {output[i][1]}, {output[i][2]}, {output[i][3]}\n"
        file.write(line)
file.close()