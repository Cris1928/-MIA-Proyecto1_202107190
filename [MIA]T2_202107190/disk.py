import os
import time
import random
import estructura
import struct
import main as main

class Disk:
    def __init__(self):
        pass
    
    @staticmethod
    def Crear():
        discoactual =estructura.MBR()
        tamdisk = 1024*1024* 5
        fit = "B"
        path = "Disc.dsk"

        discoactual.mbr_tam = tamdisk
        discoactual.mbr_creacion = int(time.time())
        discoactual.diskf= fit
        discoactual.mbr_asignaciondisk = random.randint(100, 9999)

        try:
            with open(path, "w+b") as file:
                file.write(b"\x00")
                file.seek(tamdisk - 1) # posisionado de ultimo
                file.write(b"\x00")
                file.seek(0) # posisionado al principio 
                file.write(bytes(discoactual))
            print("\n ------ MKDISK ejecutado ------- \n")

        except Exception as e:
            print(e)
            print("Error al crear el disco "+path)


    @staticmethod
    def rep():
        path ="Disc.dsk"
        try:
                FormatoDelMBR ='<iiiiB'
                TamanoDelMBR= struct.calcsize(FormatoDelMBR)
                with open(path, 'rb') as file:
                    DatosMBR=file.read(TamanoDelMBR)
                    mbr= estructura.MBR()
                    (mbr.mbr_tam, mbr.mbr_creacion, mbr.mbr_asignaciondisk, diskf, *_)= struct.unpack(FormatoDelMBR, DatosMBR)
                    mbr.diskf=chr(diskf % 128)
                print(f'\t TAMAÑO DEL DISCO : {mbr.mbr_tam}')
                print(f'\t FECHA EN QUE SE CREO : {mbr.mbr_creacion}')
                print(f'\t FIT DEL DISCO: {mbr.diskf}')
                print(f'\t DISK SIGNATURE: {mbr.mbr_asignaciondisk}')


        except Exception as e:
                print(f'\tERROR: No se puede leer el disco en la ruta: {path} debido a: {str(e)}')