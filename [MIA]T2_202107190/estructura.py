import struct

class MBR:
    def __init__(self):
        self.mbr_tamano=0
        self.mbr_fecha_creacion=0
        self.mbr_disk_signature=0
        self.disk_fit='FF' #valor por defecto first fit

    def __bytes__(self):
        return (struct.pack("<i", self.mbr_tamano)+
                struct.pack("<i", self.mbr_fecha_creacion)+
                struct.pack("<i", self.mbr_disk_signature)+
                self.disk_fit.encode('utf-8')) 