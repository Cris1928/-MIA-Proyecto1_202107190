from mkdisk import MkDisk
from rmdisk import RmDisk
from rep import reporte
 
class Scanner:

    def comand_mkdisk(self,size, unit,fit,path):
        mk = MkDisk()
        mk.fit = fit
        mk.path = path
        mk.size = size
        mk.unit = unit
        mk.create()
    def comand_rmdisk(self,path):
        rm = RmDisk()
        rm.path = path
        rm.remove()

    def comand_rep(self,path):
        repo=reporte()
        repo.path=path
        repo.rep()

    def procesar_comando(self, comando):
        datos = {} 
        if comando.startswith("mkdisk"):
            partes = comando.split()  # Dividir la cadena en palabras
        # print("abajo")
            #print(partes)
            #print("arriba")
             # Diccionario para almacenar los valores
            parametro_actual = None  # Para mantener el parámetro actual
            for palabra in partes:
                if palabra.startswith("-"):
                    parametro_actual = palabra[1:]  # Eliminar el guion (-) del parámetro
                #   print(parametro_actual)
                    parametro, valor = parametro_actual.split("=")
                    datos[parametro] = valor

                    
        #      elif parametro_actual is not None:
        #         datos[parametro_actual] = palabra
            #        print(parametro_actual)
            #       print("arriba")
            #      parametro_actual = None

        return datos
    def inicio (self):
        while True:
            print("SI DESEA TERMINAR EJECUCION INGRESE \"s\"")
            datoing = input("ingrese el comando:  ")
            if datoing.lower()== "s":
                break

            coamando=self.procesar_comando(datoing)
            if "path" in coamando and "size" in coamando:
                #si tiene path y size

                #si no tiene fit
                if "fit" not in coamando:
                    coamando["fit"]="FF"
                if "unit" not in coamando:
                    coamando["unit"]="M"
                
                #mkdisk -size=3000 -unit=K -path=Users\USER\Desktop\MIAP1_202107190\discos\discos.dk
                self.comand_mkdisk(coamando["size"],coamando["unit"],coamando["fit"],coamando["path"])
         #   print(coamando)

if __name__ == "__main__":
    scanner = Scanner()
    scanner.inicio()