import os
import struct
import time
import random
from MBR import MBR
from part import Partition
def mount(params, mounted_partitions,cont):
    filename = params.get('path')
    current_directory = os.getcwd()
    full_path= f'{filename}'
    if not os.path.exists(full_path):
        print(f"Error: el file {full_path} no existe.")
        return 
    partitions = []
    with open(full_path, "rb+") as file:
        for i in range(4):
            file.seek(struct.calcsize(MBR.FORMAT)+(i*Partition.SIZE))
            data = file.read(Partition.SIZE)
            particion_temporal = Partition.unpack(data)
            partitions.append(particion_temporal)

    name = params.get('name')
    bandera = False
    index = -50
    for i,item in enumerate(partitions):
        if item.name == name:
            bandera = True
            index = i
    if bandera == False:
        print(f"Error: la particion {name} no existe.")
        return
    mycarne = 53
    diskname = filename.split('/')[-1]
    diskname = diskname.split('.')[0]
    
    # agregar a la lista de montados
    mounted_partitions.append({id: {'path':filename , 
                                    'partition': partitions[index],
                                    'name': name,
                                    'index': index,
                                    'id': "190Disco"+str(cont),
                                    'inicio': partitions[index].byte_inicio,
                                    'size': partitions[index].actual_size,}})
    
#aqui se crea el disco
def unmount(params, mounted_partitions):
    id_to_unmount = params.get('id')
    
    for index, partition_dict in enumerate(mounted_partitions):
        if id_to_unmount in partition_dict:
            mounted_partitions.pop(index)
            print(f"particion {id_to_unmount}  desmontada.")
            return
        else:  # esto es para cuando no se encuentra la particion
            print(f"Error: la particion {id_to_unmount} no existe.")

